"""Project: Certificate Generation Lab
Institution: EK – Erhvervsakademi København
Author: moms@ek.dk
"""

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from validators import (
    clean_days,
    clean_text,
    valid_dns_name,
    valid_project_name,
    validate_algorithm,
    validate_dns_list,
    validate_ip_list,
)

BASE_DIR = Path(os.environ.get("CERT_BASE_DIR", "/app/certificates")).resolve()
DEV_BASE_DIR = Path(__file__).resolve().parent / "certificates"
if not BASE_DIR.exists() and not str(BASE_DIR).startswith("/app"):
    BASE_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOADS = {
    "ca_cert": ("ca/ca.cert.pem", "application/x-pem-file"),
    "csr": ("leaf/server.csr.pem", "application/x-pem-file"),
    "leaf_cert": ("leaf/server.cert.pem", "application/x-pem-file"),
    "server_key": ("leaf/server.key.pem", "application/x-pem-file"),
}


class CertificateError(Exception):
    pass


def ensure_base():
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def project_path(project):
    if not valid_project_name(project):
        raise CertificateError("Invalid project name. Use letters, numbers, dash, or underscore only.")
    ensure_base()
    path = (BASE_DIR / project).resolve()
    if BASE_DIR not in path.parents and path != BASE_DIR:
        raise CertificateError("Project path escaped certificate directory.")
    return path


def state_path(project):
    return project_path(project) / "project.json"


def load_state(project):
    path = state_path(project)
    if not path.exists():
        return {"project": project, "created_at": iso_now()}
    return json.loads(path.read_text())


def save_state(project, data):
    path = project_path(project)
    path.mkdir(parents=True, exist_ok=True)
    (path / "project.json").write_text(json.dumps(data, indent=2))


def list_projects():
    ensure_base()
    projects = []
    for path in sorted(BASE_DIR.iterdir()):
        if path.is_dir() and valid_project_name(path.name):
            state = load_state(path.name)
            projects.append({"name": path.name, "state": state})
    return projects


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def run_openssl(args):
    if shutil.which("openssl") is None:
        raise CertificateError("OpenSSL is not installed in this environment.")
    try:
        result = subprocess.run(
            ["openssl", *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        details = (exc.stderr or exc.stdout or "OpenSSL failed.").strip()
        raise CertificateError(details)


def subject_arg(common_name, fields):
    parts = []
    mapping = [
        ("C", "country"),
        ("ST", "state"),
        ("L", "city"),
        ("O", "organization"),
        ("OU", "unit"),
        ("emailAddress", "email"),
        ("CN", "common_name"),
    ]
    all_fields = {**fields, "common_name": common_name}
    for key, name in mapping:
        value = clean_text(all_fields.get(name, ""), 128)
        if value:
            parts.append(f"/{key}={value}")
    return "".join(parts)


def key_command(algorithm, output):
    validate_algorithm(algorithm)
    if algorithm.startswith("rsa"):
        bits = algorithm.replace("rsa", "")
        return ["genpkey", "-algorithm", "RSA", "-pkeyopt", f"rsa_keygen_bits:{bits}", "-out", str(output)]
    return ["ecparam", "-name", "prime256v1", "-genkey", "-noout", "-out", str(output)]


def ca_config(path):
    path.write_text(
        "\n".join(
            [
                "[req]",
                "distinguished_name = dn",
                "prompt = no",
                "[dn]",
                "[v3_ca]",
                "basicConstraints = critical, CA:TRUE",
                "keyUsage = critical, keyCertSign, cRLSign",
                "subjectKeyIdentifier = hash",
                "authorityKeyIdentifier = keyid:always,issuer",
                "",
            ]
        )
    )


def leaf_config(path, dns_names, ip_names, algorithm):
    san = []
    san.extend([f"DNS:{name}" for name in dns_names])
    san.extend([f"IP:{addr}" for addr in ip_names])
    key_usage = "digitalSignature"
    if algorithm.startswith("rsa"):
        key_usage += ", keyEncipherment"
    path.write_text(
        "\n".join(
            [
                "[v3_leaf]",
                "basicConstraints = critical, CA:FALSE",
                f"keyUsage = critical, {key_usage}",
                "extendedKeyUsage = serverAuth",
                f"subjectAltName = {', '.join(san)}",
                "subjectKeyIdentifier = hash",
                "authorityKeyIdentifier = keyid,issuer",
                "",
            ]
        )
    )


def csr_config(path, dns_names, ip_names):
    lines = ["[req]", "distinguished_name = dn", "req_extensions = v3_req", "prompt = no", "[dn]", "[v3_req]"]
    san = [f"DNS:{name}" for name in dns_names] + [f"IP:{addr}" for addr in ip_names]
    lines.append(f"subjectAltName = {', '.join(san)}")
    lines.append("")
    path.write_text("\n".join(lines))


def create_ca(payload):
    project = clean_text(payload.get("project", ""), 64)
    if not valid_project_name(project):
        raise CertificateError("Invalid project name. Use letters, numbers, dash, or underscore only.")
    ca_name = clean_text(payload.get("ca_name", ""), 128)
    if not ca_name:
        raise CertificateError("CA Name is required.")
    days = clean_days(payload.get("days"), 3650)
    algorithm = validate_algorithm(payload.get("algorithm", "rsa3072"))
    fields = clean_fields(payload)
    root = project_path(project)
    ca_dir = root / "ca"
    ca_dir.mkdir(parents=True, exist_ok=True)
    key = ca_dir / "ca.key.pem"
    cert = ca_dir / "ca.cert.pem"
    ext = ca_dir / "ca.ext"
    ca_config(ext)
    commands = []
    key_cmd = key_command(algorithm, key)
    run_openssl(key_cmd)
    commands.append(["openssl", *key_cmd])
    cert_cmd = [
        "req",
        "-x509",
        "-new",
        "-key",
        str(key),
        "-sha256",
        "-days",
        str(days),
        "-subj",
        subject_arg(ca_name, fields),
        "-out",
        str(cert),
        "-config",
        str(ext),
        "-extensions",
        "v3_ca",
    ]
    run_openssl(cert_cmd)
    commands.append(["openssl", *cert_cmd])
    state = load_state(project)
    for key_name in [
        "trust_step_completed",
        "csr_created",
        "leaf_signed",
        "hostname",
        "dns_names",
        "ip_names",
        "leaf_algorithm",
        "commands_leaf",
        "commands_sign",
    ]:
        state.pop(key_name, None)
    state.update(
        {
            "project": project,
            "ca_created": True,
            "ca_name": ca_name,
            "ca_algorithm": algorithm,
            "ca_days": days,
            "updated_at": iso_now(),
            "commands_ca": commands,
        }
    )
    save_state(project, state)
    return {"state": state, "info": inspect_certificate(project, "ca_cert"), "commands": commands}


def create_leaf(payload):
    project = clean_text(payload.get("project", ""), 64)
    root = project_path(project)
    if not (root / "ca/ca.cert.pem").exists():
        raise CertificateError("Create the CA before creating a CSR.")
    hostname = clean_text(payload.get("hostname", ""), 128)
    if not valid_dns_name(hostname):
        raise CertificateError("Primary DNS name / hostname is required and must be valid.")
    dns_names = validate_dns_list(payload.get("dns_names", []))
    ip_names = validate_ip_list(payload.get("ip_names", []))
    if hostname and hostname not in dns_names:
        dns_names.insert(0, hostname)
    if not dns_names and not ip_names:
        raise CertificateError("At least one DNS or IP SAN is required.")
    algorithm = validate_algorithm(payload.get("algorithm", "rsa2048"))
    fields = clean_fields(payload)
    leaf_dir = root / "leaf"
    leaf_dir.mkdir(parents=True, exist_ok=True)
    key = leaf_dir / "server.key.pem"
    csr = leaf_dir / "server.csr.pem"
    conf = leaf_dir / "server-csr.cnf"
    csr_config(conf, dns_names, ip_names)
    commands = []
    key_cmd = key_command(algorithm, key)
    run_openssl(key_cmd)
    commands.append(["openssl", *key_cmd])
    csr_cmd = [
        "req",
        "-new",
        "-key",
        str(key),
        "-subj",
        subject_arg(hostname or dns_names[0], fields),
        "-out",
        str(csr),
        "-config",
        str(conf),
    ]
    run_openssl(csr_cmd)
    commands.append(["openssl", *csr_cmd])
    state = load_state(project)
    state.pop("leaf_signed", None)
    state.pop("commands_sign", None)
    state.update(
        {
            "csr_created": True,
            "hostname": hostname or dns_names[0],
            "dns_names": dns_names,
            "ip_names": ip_names,
            "leaf_algorithm": algorithm,
            "updated_at": iso_now(),
            "commands_leaf": commands,
        }
    )
    save_state(project, state)
    return {"state": state, "info": inspect_csr(project), "commands": commands}


def sign_leaf(payload):
    project = clean_text(payload.get("project", ""), 64)
    root = project_path(project)
    state = load_state(project)
    required = [root / "ca/ca.cert.pem", root / "ca/ca.key.pem", root / "leaf/server.csr.pem"]
    if not all(path.exists() for path in required):
        raise CertificateError("Create the CA and CSR before signing.")
    dns_names = state.get("dns_names", [])
    ip_names = state.get("ip_names", [])
    leaf_algorithm = state.get("leaf_algorithm", "rsa2048")
    cert = root / "leaf/server.cert.pem"
    ext = root / "leaf/server-cert.ext"
    leaf_config(ext, dns_names, ip_names, leaf_algorithm)
    cmd = [
        "x509",
        "-req",
        "-in",
        str(root / "leaf/server.csr.pem"),
        "-CA",
        str(root / "ca/ca.cert.pem"),
        "-CAkey",
        str(root / "ca/ca.key.pem"),
        "-CAcreateserial",
        "-out",
        str(cert),
        "-days",
        "825",
        "-sha256",
        "-extfile",
        str(ext),
        "-extensions",
        "v3_leaf",
    ]
    run_openssl(cmd)
    state.update({"leaf_signed": True, "updated_at": iso_now(), "commands_sign": [["openssl", *cmd]]})
    save_state(project, state)
    return {"state": state, "info": inspect_certificate(project, "leaf_cert"), "commands": [["openssl", *cmd]]}


def complete_trust(project):
    state = load_state(project)
    state["trust_step_completed"] = True
    state["updated_at"] = iso_now()
    save_state(project, state)
    return state


def clean_fields(payload):
    return {
        "country": clean_text(payload.get("country", ""), 2),
        "state": clean_text(payload.get("state", ""), 128),
        "city": clean_text(payload.get("city", ""), 128),
        "organization": clean_text(payload.get("organization", ""), 128),
        "unit": clean_text(payload.get("unit", ""), 128),
        "email": clean_text(payload.get("email", ""), 128),
    }


def known_file(project, file_id):
    if file_id not in DOWNLOADS:
        raise CertificateError("Unknown download.")
    rel, mimetype = DOWNLOADS[file_id]
    root = project_path(project)
    path = (root / rel).resolve()
    if root not in path.parents:
        raise CertificateError("Download path escaped project directory.")
    if not path.exists():
        raise CertificateError("File has not been generated yet.")
    return path, mimetype


def raw_output(project, kind):
    path, _ = known_file(project, kind)
    if kind == "csr":
        return run_openssl(["req", "-in", str(path), "-text", "-noout"])
    return run_openssl(["x509", "-in", str(path), "-text", "-noout"])


def inspect_certificate(project, kind):
    path, _ = known_file(project, kind)
    text = raw_output(project, kind)
    subject = run_openssl(["x509", "-in", str(path), "-noout", "-subject"]).replace("subject=", "").strip()
    issuer = run_openssl(["x509", "-in", str(path), "-noout", "-issuer"]).replace("issuer=", "").strip()
    serial = run_openssl(["x509", "-in", str(path), "-noout", "-serial"]).replace("serial=", "").strip()
    dates = run_openssl(["x509", "-in", str(path), "-noout", "-dates"]).splitlines()
    fingerprint = run_openssl(["x509", "-in", str(path), "-noout", "-fingerprint", "-sha256"]).replace("sha256 Fingerprint=", "").replace("SHA256 Fingerprint=", "").strip()
    return {
        "subject": subject,
        "issuer": issuer,
        "serial": serial,
        "valid_from": dates[0].replace("notBefore=", "") if dates else "",
        "valid_until": dates[1].replace("notAfter=", "") if len(dates) > 1 else "",
        "public_key": find_value(text, "Public Key Algorithm:"),
        "key_size": parse_key_size(text),
        "signature_algorithm": find_value(text, "Signature Algorithm:"),
        "basic_constraints": extract_block_line(text, "Basic Constraints"),
        "key_usage": extract_block_line(text, "Key Usage"),
        "extended_key_usage": extract_block_line(text, "Extended Key Usage"),
        "sans": parse_sans(text),
        "fingerprint": fingerprint,
    }


def inspect_csr(project):
    text = raw_output(project, "csr")
    root = project_path(project)
    csr = root / "leaf/server.csr.pem"
    subject = run_openssl(["req", "-in", str(csr), "-noout", "-subject"]).replace("subject=", "").strip()
    return {
        "subject": subject,
        "public_key": find_value(text, "Public Key Algorithm:"),
        "key_size": parse_key_size(text),
        "requested_extensions": "Requested Extensions" if "Requested Extensions" in text else "",
        "sans": parse_sans(text),
    }


def find_value(text, marker):
    for line in text.splitlines():
        if marker in line:
            return line.split(marker, 1)[1].strip()
    return ""


def parse_key_size(text):
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Public-Key:"):
            return line.replace("Public-Key:", "").strip().strip("()")
        if line.startswith("ASN1 OID:"):
            return line.replace("ASN1 OID:", "").strip()
    return ""


def extract_block_line(text, title):
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if title in line:
            if idx + 1 < len(lines):
                return lines[idx + 1].strip()
    return ""


def parse_sans(text):
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if "Subject Alternative Name" in line and idx + 1 < len(lines):
            return [item.strip() for item in lines[idx + 1].split(",")]
    return []
