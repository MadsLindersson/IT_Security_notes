"""Restore the reduced Part III baseline before starting the GUI."""
import json
from pathlib import Path
from network import ensure_firewall_chain, run_cmd

ensure_firewall_chain()
run_cmd(["iptables", "-P", "FORWARD", "DROP"])
run_cmd(["iptables", "-F", "MOSEC_ACL"])
for rule in json.loads(Path("/app/part3-policy.json").read_text()):
    run_cmd(["iptables", "-A", "MOSEC_ACL", *rule])

# Also restored by GUI firewall/router reset in Part IV mode.
import os
if os.environ.get("PART4_AUTOCONFIG") == "1":
    run_cmd(["python", "/app/init-part4.py"])

# Enable forwarding only after the complete baseline and NAT are installed.
run_cmd(["sysctl", "-w", "net.ipv4.ip_forward=1"])
