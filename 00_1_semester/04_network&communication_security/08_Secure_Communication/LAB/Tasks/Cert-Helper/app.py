"""Project: Certificate Generation Lab
Institution: EK – Erhvervsakademi København
Author: moms@ek.dk
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for

load_dotenv()

# The certificate service reads CERT_BASE_DIR when it is imported.
import certificate_service as certs

app = Flask(__name__)


@app.get("/")
def index():
    projects = certs.list_projects()
    return render_template("index.html", projects=projects)


@app.get("/beginner")
def beginner():
    project = request.args.get("project", "")
    state = {}
    if project:
        try:
            state = certs.load_state(project)
        except certs.CertificateError:
            project = ""
    return render_template("beginner.html", project=project, state=state)


@app.get("/beginner/create-ca")
def create_ca_page():
    return redirect(url_for("beginner"))


@app.get("/beginner/trust-ca")
def trust_ca_page():
    return redirect(url_for("beginner"))


@app.get("/beginner/create-leaf")
def create_leaf_page():
    return redirect(url_for("beginner"))


@app.get("/beginner/sign-leaf")
def sign_leaf_page():
    return redirect(url_for("beginner"))


@app.get("/beginner/summary")
def summary_page():
    return redirect(url_for("beginner"))


@app.get("/advanced")
def advanced():
    return render_template("advanced.html")


@app.get("/inspector")
def inspector():
    return render_template("inspector.html", projects=certs.list_projects())


@app.post("/api/create-ca")
def api_create_ca():
    return api_response(certs.create_ca)


@app.post("/api/create-leaf")
def api_create_leaf():
    return api_response(certs.create_leaf)


@app.post("/api/sign-leaf")
def api_sign_leaf():
    return api_response(certs.sign_leaf)


@app.post("/api/trust-complete")
def api_trust_complete():
    data = request.get_json(force=True)
    try:
        return jsonify({"ok": True, "state": certs.complete_trust(data.get("project", ""))})
    except certs.CertificateError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.get("/api/project/<project>")
def api_project(project):
    try:
        return jsonify({"ok": True, "state": certs.load_state(project)})
    except certs.CertificateError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.get("/api/inspect/<project>/<kind>")
def api_inspect(project, kind):
    try:
        if kind == "csr":
            info = certs.inspect_csr(project)
        elif kind in {"ca_cert", "leaf_cert"}:
            info = certs.inspect_certificate(project, kind)
        else:
            raise certs.CertificateError("Unknown inspection target.")
        raw = certs.raw_output(project, kind) if request.args.get("raw") == "1" else ""
        return jsonify({"ok": True, "info": info, "raw": raw})
    except certs.CertificateError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.get("/download/<project>/<file_id>")
def download(project, file_id):
    try:
        path, mimetype = certs.known_file(project, file_id)
        return send_file(path, mimetype=mimetype, as_attachment=True, download_name=path.name)
    except certs.CertificateError as exc:
        return str(exc), 404


def api_response(handler):
    data = request.get_json(force=True)
    try:
        return jsonify({"ok": True, **handler(data)})
    except certs.CertificateError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


if __name__ == "__main__":
    app.run(
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "9090")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
