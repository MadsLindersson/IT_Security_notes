import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

import network


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "lab-only-secret")


def require_login(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def handle_network_action(action):
    try:
        action()
        flash("Change applied.", "success")
    except Exception as exc:
        flash(str(exc), "error")


@app.get("/login")
def login():
    return render_template("login.html")


@app.post("/login")
def login_post():
    username = os.environ.get("ROUTER_USERNAME", "admin")
    password = os.environ.get("ROUTER_PASSWORD", "admin")
    if request.form.get("username") == username and request.form.get("password") == password:
        session["logged_in"] = True
        return redirect(url_for("dashboard"))
    flash("Invalid credentials.", "error")
    return redirect(url_for("login"))


@app.post("/logout")
@require_login
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/")
@require_login
def dashboard():
    return render_template(
        "dashboard.html",
        title="Dashboard",
        hostname=network.hostname(),
        forwarding=network.ip_forwarding_enabled(),
        wan_up=network.wan_up(),
        nat=network.nat_enabled(),
        interfaces=network.interfaces(),
    )


@app.get("/interfaces")
@require_login
def interfaces():
    return render_template("interfaces.html", title="Interfaces", interfaces=network.interfaces())


@app.post("/interfaces/update")
@require_login
def update_interface():
    handle_network_action(lambda: network.configure_interface(
        request.form.get("role", ""),
        request.form.get("address", ""),
        request.form.get("prefix", ""),
    ))
    return redirect(url_for("interfaces"))


@app.get("/routing")
@require_login
def routing():
    return render_template(
        "routing.html",
        title="Routing",
        routes=network.routes(),
        default_route=network.default_route(),
        interfaces=network.interfaces(),
        forwarding=network.ip_forwarding_enabled(),
    )


@app.post("/routing/forwarding")
@require_login
def set_forwarding():
    handle_network_action(lambda: network.set_ip_forwarding(request.form.get("enabled") == "1"))
    return redirect(url_for("routing"))


@app.post("/routing/static/add")
@require_login
def add_route():
    handle_network_action(lambda: network.add_static_route(
        request.form.get("destination", ""),
        request.form.get("gateway", ""),
        request.form.get("interface", ""),
    ))
    return redirect(url_for("routing"))


@app.post("/routing/static/delete")
@require_login
def delete_route():
    handle_network_action(lambda: network.delete_static_route(
        request.form.get("destination", ""),
        request.form.get("gateway", ""),
        request.form.get("interface", ""),
    ))
    return redirect(url_for("routing"))


@app.get("/nat")
@require_login
def nat():
    return render_template(
        "nat.html",
        title="NAT",
        nat=network.nat_enabled(),
        wan=network.interface_by_role("WAN"),
        counters=network.nat_counters(),
    )


@app.get("/firewall")
@require_login
def firewall():
    rules = network.firewall_rules()
    return render_template(
        "firewall.html",
        title="Firewall / ACL",
        effective_rules=rules,
        acl_rules=[rule for rule in rules if rule["rule_type"] == "ACL"],
        firewall_rules=[rule for rule in rules if rule["rule_type"] == "Firewall"],
        zones=network.firewall_zones(),
        firewall_enabled=network.firewall_enabled(),
        default_action=network.firewall_default_action(),
    )


@app.post("/firewall/add")
@require_login
def firewall_add():
    handle_network_action(lambda: network.add_firewall_rule(
        request.form.get("action", ""),
        request.form.get("source", ""),
        request.form.get("destination", ""),
        request.form.get("protocol", "ANY"),
        request.form.get("zone", ""),
        request.form.get("description", ""),
        request.form.get("destination_port", ""),
        request.form.get("state", "ANY"),
    ))
    return redirect(url_for("firewall"))


@app.post("/firewall/delete")
@require_login
def firewall_delete():
    handle_network_action(lambda: network.delete_firewall_rule(request.form.get("line", "")))
    return redirect(url_for("firewall"))


@app.post("/firewall/move")
@require_login
def firewall_move():
    handle_network_action(lambda: network.move_firewall_rule(
        request.form.get("line", ""),
        request.form.get("direction", ""),
    ))
    return redirect(url_for("firewall"))


@app.post("/firewall/reset")
@require_login
def firewall_reset():
    handle_network_action(network.reset_firewall)
    return redirect(url_for("firewall"))


@app.get("/help")
@require_login
def help_page():
    return render_template("help.html", title="Help")


@app.post("/nat/toggle")
@require_login
def nat_toggle():
    enabled = request.form.get("enabled") == "1"
    handle_network_action(network.enable_nat if enabled else network.disable_nat)
    return redirect(url_for("nat"))


@app.post("/reset")
@require_login
def reset():
    if request.form.get("confirm") != "RESET":
        flash("Type RESET to confirm.", "error")
    else:
        handle_network_action(network.reset_router)
    return redirect(url_for("dashboard"))
