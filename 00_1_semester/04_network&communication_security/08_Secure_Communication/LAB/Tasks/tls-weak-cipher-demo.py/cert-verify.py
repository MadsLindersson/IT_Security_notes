#!/usr/bin/env python3

import os
import re
import ssl
import socket
import subprocess
import tempfile
from pathlib import Path


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def run(cmd, input_text=None):
    """Run a command and return stdout + stderr."""
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return result.returncode, result.stdout


def extract_pem_certificates(text):
    """Extract all PEM certificates from openssl output."""
    pattern = re.compile(
        r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
        re.DOTALL
    )
    return pattern.findall(text)


def openssl_x509(cert_file, *args):
    cmd = ["openssl", "x509", "-in", str(cert_file)] + list(args)
    rc, output = run(cmd)
    return output.strip()


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ------------------------------------------------------------
# Certificate information
# ------------------------------------------------------------

def print_certificate_info(cert_file, number, role):
    section(f"CERTIFICATE #{number} — {role}")

    subject = openssl_x509(cert_file, "-noout", "-subject")
    issuer = openssl_x509(cert_file, "-noout", "-issuer")
    dates = openssl_x509(cert_file, "-noout", "-dates")
    serial = openssl_x509(cert_file, "-noout", "-serial")
    fingerprint = openssl_x509(
        cert_file,
        "-noout",
        "-fingerprint",
        "-sha256"
    )

    print(subject)
    print(issuer)
    print(serial)
    print(dates)
    print(fingerprint)

    # Subject Alternative Names
    san = openssl_x509(
        cert_file,
        "-noout",
        "-ext",
        "subjectAltName"
    )

    print("\nSubject Alternative Names:")
    print(san if san else "Not present")

    # Basic constraints tells us whether this is a CA
    constraints = openssl_x509(
        cert_file,
        "-noout",
        "-ext",
        "basicConstraints"
    )

    print("\nBasic Constraints:")
    print(constraints if constraints else "Not present")

    # Extract signature algorithm
    full_text = openssl_x509(cert_file, "-noout", "-text")

    algorithms = re.findall(
        r"Signature Algorithm:\s*(.+)",
        full_text
    )

    if algorithms:
        print("\nCertificate Signature Algorithm:")
        print(algorithms[0].strip())

    # Public-key information
    pubkey_match = re.search(
        r"Public Key Algorithm:\s*(.+)",
        full_text
    )

    if pubkey_match:
        print("\nPublic Key Algorithm:")
        print(pubkey_match.group(1).strip())

    bits_match = re.search(
        r"Public-Key:\s*\((\d+)\s+bit\)",
        full_text
    )

    if bits_match:
        print("Public Key Size:")
        print(bits_match.group(1), "bits")


# ------------------------------------------------------------
# Extract issuer public key
# ------------------------------------------------------------

def show_issuer_public_key(cert_file, label):
    section(f"PUBLIC KEY USED TO VERIFY — {label}")

    rc, pubkey = run([
        "openssl",
        "x509",
        "-in",
        str(cert_file),
        "-pubkey",
        "-noout"
    ])

    if rc != 0:
        print("Could not extract public key.")
        return

    print(pubkey.strip())

    print(
        "\nThis public key belongs to the certificate issuer/CA and can "
        "be used by OpenSSL when checking certificates signed by that CA."
    )


# ------------------------------------------------------------
# TLS connection
# ------------------------------------------------------------

def fetch_server_chain(domain, port):
    section("1. CONNECTING TO SERVER")

    print(f"Domain : {domain}")
    print(f"Port   : {port}")
    print()

    try:
        ip = socket.gethostbyname(domain)
        print(f"Resolved IP: {ip}")
    except socket.gaierror:
        print("DNS resolution failed.")
        return None

    print("\nRequesting TLS certificate chain...")

    cmd = [
        "openssl",
        "s_client",
        "-connect",
        f"{domain}:{port}",
        "-servername",
        domain,
        "-showcerts"
    ]

    rc, output = run(cmd, "")

    certs = extract_pem_certificates(output)

    if not certs:
        print("No certificates received.")
        return None

    print(f"Received {len(certs)} certificate(s) from server.")

    return certs


# ------------------------------------------------------------
# Certificate verification
# ------------------------------------------------------------

def verify_chain(domain, leaf, intermediates):
    section("4. VERIFY CERTIFICATE CHAIN")

    verify_paths = ssl.get_default_verify_paths()

    print("System trust configuration:")

    if verify_paths.cafile:
        print(" CA file :", verify_paths.cafile)

    if verify_paths.capath:
        print(" CA path :", verify_paths.capath)

    cmd = [
        "openssl",
        "verify",
        "-show_chain",
        "-purpose",
        "sslserver",
        "-verify_hostname",
        domain
    ]

    # Use operating system / Python OpenSSL trust store
    if verify_paths.cafile and os.path.exists(verify_paths.cafile):
        cmd += ["-CAfile", verify_paths.cafile]

    elif verify_paths.capath and os.path.exists(verify_paths.capath):
        cmd += ["-CApath", verify_paths.capath]

    # Intermediate certificates supplied by server
    if intermediates:
        intermediate_bundle = leaf.parent / "intermediates.pem"

        with open(intermediate_bundle, "w") as f:
            for cert in intermediates:
                f.write(Path(cert).read_text())
                f.write("\n")

        cmd += ["-untrusted", str(intermediate_bundle)]

    cmd.append(str(leaf))

    print("\nRunning verification:\n")
    print(" ".join(cmd))
    print()

    rc, output = run(cmd)

    print(output.strip())

    print()

    if rc == 0:
        print("RESULT: CERTIFICATE VERIFIED ✓")
        print()
        print(
            "OpenSSL successfully built a chain from the server "
            "certificate to a trusted Root CA."
        )
    else:
        print("RESULT: CERTIFICATE VERIFICATION FAILED ✗")


# ------------------------------------------------------------
# Explain signature relationship
# ------------------------------------------------------------

def explain_chain(cert_files):
    section("3. SIGNATURE RELATIONSHIP")

    for i in range(len(cert_files) - 1):
        child = cert_files[i]
        issuer = cert_files[i + 1]

        child_subject = openssl_x509(
            child,
            "-noout",
            "-subject"
        )

        issuer_subject = openssl_x509(
            issuer,
            "-noout",
            "-subject"
        )

        print(f"Certificate #{i + 1}")
        print(f"  {child_subject}")
        print()
        print("        signed by")
        print("            ↓")
        print()
        print(f"Certificate #{i + 2}")
        print(f"  {issuer_subject}")
        print()

    print(
        "The issuer signs a certificate using its PRIVATE key.\n"
        "The client verifies that signature using the issuer's PUBLIC key."
    )


# ------------------------------------------------------------
# Main application
# ------------------------------------------------------------

def main():

    print("""
============================================================
        TLS / X.509 Certificate Teaching Tool
============================================================

This program will:

  1. Connect to a HTTPS server
  2. Download the certificate chain supplied by the server
  3. Display certificate details
  4. Show intermediate CA information
  5. Show signature algorithms
  6. Extract CA public keys
  7. Verify the certificate chain against the local trust store
""")

    domain = input(
        "Enter domain (example: ek.dk): "
    ).strip()

    if not domain:
        print("No domain entered.")
        return

    port_input = input(
        "Port [443]: "
    ).strip()

    port = int(port_input) if port_input else 443

    certs = fetch_server_chain(domain, port)

    if not certs:
        return

    with tempfile.TemporaryDirectory() as temp:

        temp_path = Path(temp)
        cert_files = []

        # Save certificates individually
        for i, cert in enumerate(certs):

            filename = temp_path / f"certificate-{i}.pem"

            filename.write_text(cert)

            cert_files.append(filename)

        section("2. CERTIFICATES SENT BY SERVER")

        print(
            "Important: HTTPS servers normally send the server certificate\n"
            "and intermediate CA certificates. The Root CA is normally NOT\n"
            "sent because the client already has trusted roots locally."
        )

        # Print all certificates
        for i, cert_file in enumerate(cert_files):

            if i == 0:
                role = "SERVER / LEAF CERTIFICATE"
            else:
                role = "INTERMEDIATE CA"

            print_certificate_info(
                cert_file,
                i + 1,
                role
            )

        # Explain chain
        explain_chain(cert_files)

        # Show public key of each issuer/intermediate
        if len(cert_files) > 1:

            for i in range(1, len(cert_files)):

                show_issuer_public_key(
                    cert_files[i],
                    f"Certificate #{i + 1}"
                )

        else:
            section("INTERMEDIATE CA")

            print(
                "The server did not provide an intermediate CA certificate."
            )

        # Verify
        leaf = cert_files[0]
        intermediates = cert_files[1:]

        verify_chain(
            domain,
            leaf,
            intermediates
        )


if __name__ == "__main__":
    main()