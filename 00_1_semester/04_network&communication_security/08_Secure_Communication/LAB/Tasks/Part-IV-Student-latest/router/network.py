import ipaddress
import json
import os
import shlex
import socket
import subprocess


APP_NAT_CHAIN = "MOSEC_NAT"
APP_FW_CHAIN = "MOSEC_ACL"


class NetworkError(RuntimeError):
    pass


def run_cmd(args, check=True):
    result = subprocess.run(args, check=False, text=True, capture_output=True)
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "command failed"
        raise NetworkError(message)
    return result.stdout


def parse_role_interfaces():
    raw = os.environ.get("ROLE_INTERFACES", "")
    mappings = {}
    for item in raw.split(","):
        if not item.strip():
            continue
        role, iface = item.split("=", 1)
        mappings[role.strip()] = iface.strip()
    return mappings


def wan_name():
    return os.environ.get("WAN_INTERFACE", "eth0")


def ip_addr_json():
    return json.loads(run_cmd(["ip", "-j", "addr", "show"]))


def interfaces():
    role_interfaces = parse_role_interfaces()
    iface_roles = {iface: role for role, iface in role_interfaces.items()}
    iface_roles[wan_name()] = "WAN"
    discovered = {iface["ifname"]: iface for iface in ip_addr_json()}
    rows = []
    for name, role in iface_roles.items():
        iface = discovered.get(name)
        if not iface:
            rows.append({
                "name": name,
                "role": role,
                "address": "",
                "prefix": "",
                "cidr": "",
                "state": "MISSING",
                "network": "",
                "configured": False,
            })
            continue
        ipv4_rows = [
            addr for addr in iface.get("addr_info", [])
            if addr.get("family") == "inet"
        ]
        if ipv4_rows:
            addr = ipv4_rows[0]
            address = ipaddress.ip_address(addr["local"])
            prefix = int(addr["prefixlen"])
            rows.append({
                "name": name,
                "role": role,
                "address": str(address),
                "prefix": prefix,
                "cidr": f"{address}/{prefix}",
                "state": iface.get("operstate", "UNKNOWN"),
                "network": str(ipaddress.ip_network(f"{address}/{prefix}", strict=False)),
                "configured": True,
            })
        else:
            rows.append({
                "name": name,
                "role": role,
                "address": "",
                "prefix": "",
                "cidr": "",
                "state": iface.get("operstate", "UNKNOWN"),
                "network": "",
                "configured": False,
            })
    rows.sort(key=lambda row: role_sort(row["role"]))
    return rows


def role_sort(role):
    order = {"WAN": 0, "Admin": 1, "Employee": 2, "Server": 3, "Guest": 4, "Printer": 5}
    return order.get(role, 99)


def interface_by_role(role):
    for iface in interfaces():
        if iface["role"].lower() == role.lower():
            return iface
    return None


def wan_interface():
    return wan_name()


def ip_forwarding_enabled():
    value = run_cmd(["sysctl", "-n", "net.ipv4.ip_forward"]).strip()
    return value == "1"


def set_ip_forwarding(enabled):
    value = "1" if enabled else "0"
    run_cmd(["sysctl", "-w", f"net.ipv4.ip_forward={value}"])


def hostname():
    return socket.gethostname()


def ip_route_lines():
    return [line for line in run_cmd(["ip", "route", "show"]).splitlines() if line.strip()]


def routes():
    iface_roles = {row["name"]: row["role"] for row in interfaces()}
    parsed = []
    for line in ip_route_lines():
        tokens = line.split()
        destination = tokens[0]
        if destination == "default":
            destination = "0.0.0.0/0"
            route_type = "Default"
        elif "proto" in tokens and "kernel" in tokens:
            route_type = "Connected"
        elif "scope" in tokens and "link" in tokens and "src" in tokens:
            route_type = "Connected"
        else:
            route_type = "Static"

        gateway = "directly connected"
        if "via" in tokens:
            gateway = tokens[tokens.index("via") + 1]

        dev = ""
        if "dev" in tokens:
            dev = tokens[tokens.index("dev") + 1]

        parsed.append({
            "destination": destination,
            "gateway": gateway,
            "interface": dev,
            "role": iface_roles.get(dev, dev or "Unknown"),
            "type": route_type,
            "raw": line,
            "deletable": route_type == "Static" and destination != "0.0.0.0/0",
        })
    return parsed


def default_route():
    for route in routes():
        if route["type"] == "Default":
            return route
    return None


def validate_destination(value):
    return ipaddress.ip_network(value.strip(), strict=False)


def validate_gateway(value):
    return ipaddress.ip_address(value.strip())


def validate_interface_name(value):
    if not value:
        return ""
    names = {iface["name"] for iface in interfaces()}
    if value not in names:
        raise NetworkError("Unknown interface")
    return value


def add_static_route(destination, gateway, interface_name=""):
    network = validate_destination(destination)
    gw = validate_gateway(gateway)
    dev = validate_interface_name(interface_name.strip())
    args = ["ip", "route", "add", str(network), "via", str(gw), "proto", "static"]
    if dev:
        args.extend(["dev", dev])
    run_cmd(args)


def delete_static_route(destination, gateway, interface_name=""):
    network = validate_destination(destination)
    gw = validate_gateway(gateway)
    dev = validate_interface_name(interface_name.strip())
    args = ["ip", "route", "del", str(network), "via", str(gw)]
    if dev:
        args.extend(["dev", dev])
    run_cmd(args)


def configure_interface(role, address, prefix):
    iface = interface_by_role(role)
    if not iface:
        raise NetworkError("Role interface was not found")
    if role.lower() == "wan":
        raise NetworkError("The WAN/management interface is not part of the exercise")
    ip = ipaddress.ip_address(address.strip())
    prefix_int = int(prefix)
    if prefix_int < 1 or prefix_int > 32:
        raise NetworkError("CIDR prefix must be between 1 and 32")
    run_cmd(["ip", "addr", "replace", f"{ip}/{prefix_int}", "dev", iface["name"]])


def chain_exists(chain):
    result = subprocess.run(
        ["iptables", "-t", "nat", "-n", "-L", chain],
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def filter_chain_exists(chain):
    result = subprocess.run(
        ["iptables", "-n", "-L", chain],
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def ensure_nat_chain():
    if not chain_exists(APP_NAT_CHAIN):
        run_cmd(["iptables", "-t", "nat", "-N", APP_NAT_CHAIN])


def has_postrouting_jump():
    result = subprocess.run(
        ["iptables", "-t", "nat", "-C", "POSTROUTING", "-j", APP_NAT_CHAIN],
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def has_masquerade_rule(out_iface):
    result = subprocess.run(
        ["iptables", "-t", "nat", "-C", APP_NAT_CHAIN, "-o", out_iface, "-j", "MASQUERADE"],
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def nat_enabled():
    try:
        out_iface = wan_interface()
    except NetworkError:
        return False
    return chain_exists(APP_NAT_CHAIN) and has_postrouting_jump() and has_masquerade_rule(out_iface)


def enable_nat():
    out_iface = wan_interface()
    ensure_nat_chain()
    if not has_postrouting_jump():
        run_cmd(["iptables", "-t", "nat", "-A", "POSTROUTING", "-j", APP_NAT_CHAIN])
    if not has_masquerade_rule(out_iface):
        run_cmd(["iptables", "-t", "nat", "-A", APP_NAT_CHAIN, "-o", out_iface, "-j", "MASQUERADE"])


def disable_nat():
    if chain_exists(APP_NAT_CHAIN):
        out_iface = wan_interface()
        while has_masquerade_rule(out_iface):
            run_cmd(["iptables", "-t", "nat", "-D", APP_NAT_CHAIN, "-o", out_iface, "-j", "MASQUERADE"])
        while has_postrouting_jump():
            run_cmd(["iptables", "-t", "nat", "-D", "POSTROUTING", "-j", APP_NAT_CHAIN])
        run_cmd(["iptables", "-t", "nat", "-F", APP_NAT_CHAIN])
        run_cmd(["iptables", "-t", "nat", "-X", APP_NAT_CHAIN])


def nat_counters():
    if not chain_exists(APP_NAT_CHAIN):
        return {"packets": 0, "bytes": 0}
    out = run_cmd(["iptables", "-t", "nat", "-L", APP_NAT_CHAIN, "-n", "-v", "-x"])
    for line in out.splitlines():
        if "MASQUERADE" in line:
            parts = line.split()
            return {"packets": int(parts[0]), "bytes": int(parts[1])}
    return {"packets": 0, "bytes": 0}


def wan_up():
    try:
        iface = interface_by_role("WAN")
        return bool(iface and iface["state"].upper() == "UP")
    except NetworkError:
        return False


def has_forward_jump():
    result = subprocess.run(
        ["iptables", "-C", "FORWARD", "-j", APP_FW_CHAIN],
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def firewall_enabled():
    return True


def firewall_default_action():
    return "DENY"


def ensure_firewall_chain():
    if not filter_chain_exists(APP_FW_CHAIN):
        run_cmd(["iptables", "-N", APP_FW_CHAIN])
    if not has_forward_jump():
        run_cmd(["iptables", "-I", "FORWARD", "1", "-j", APP_FW_CHAIN])


def firewall_zones():
    rows = []
    for iface in interfaces():
        if iface["role"] in {"WAN", "Admin", "Employee", "Server", "Guest", "Printer"}:
            rows.append({"role": iface["role"], "name": iface["name"]})
    rows.sort(key=lambda row: role_sort(row["role"]))
    return rows


def validate_firewall_action(value):
    action = value.strip().upper()
    if action not in {"ALLOW", "DENY"}:
        raise NetworkError("Action must be ALLOW or DENY")
    return action


def validate_firewall_protocol(value):
    protocol = value.strip().upper()
    if protocol not in {"ANY", "TCP", "UDP", "ICMP"}:
        raise NetworkError("Protocol must be ANY, TCP, UDP, or ICMP")
    return protocol


def validate_firewall_port(value, protocol):
    raw = value.strip()
    if not raw:
        return ""
    if protocol not in {"TCP", "UDP"}:
        raise NetworkError("Destination port can only be used with TCP or UDP")
    if not raw.isdigit():
        raise NetworkError("Destination port must be a number")
    port = int(raw)
    if port < 1 or port > 65535:
        raise NetworkError("Destination port must be between 1 and 65535")
    return str(port)


def validate_firewall_state(value):
    state = value.strip().upper()
    if not state:
        state = "ANY"
    if state not in {"ANY", "NEW", "ESTABLISHED", "RELATED"}:
        raise NetworkError("Connection state must be ANY, NEW, ESTABLISHED, or RELATED")
    return state


def validate_firewall_zone(value):
    zone = value.strip()
    if not zone:
        return "", ""
    for item in firewall_zones():
        if item["role"] == zone:
            return item["role"], item["name"]
    raise NetworkError("Unknown incoming zone")


def validate_firewall_description(value):
    description = value.strip()
    if len(description) > 30:
        raise NetworkError("Description must be 30 characters or fewer")
    if "|" in description:
        raise NetworkError("Description cannot contain |")
    if any(ord(char) < 32 for char in description):
        raise NetworkError("Description cannot contain control characters")
    return description


def add_firewall_rule(action, source, destination, protocol, zone, description="", destination_port="", state="ANY"):
    action = validate_firewall_action(action)
    source_net = ipaddress.ip_network(source.strip(), strict=False)
    destination_net = ipaddress.ip_network(destination.strip(), strict=False)
    zone_role, zone_iface = validate_firewall_zone(zone)
    if zone_iface:
        protocol = validate_firewall_protocol(protocol)
        destination_port = validate_firewall_port(destination_port, protocol)
        state = validate_firewall_state(state)
    else:
        protocol = "ANY"
        destination_port = ""
        state = "ANY"
    description = validate_firewall_description(description)

    ensure_firewall_chain()
    target = "ACCEPT" if action == "ALLOW" else "DROP"
    comment_zone = zone_role or "Any"
    rule_type = "Firewall" if zone_iface else "ACL"
    comment = f"MOSEC|{action}|{source_net}|{destination_net}|{protocol}|{comment_zone}|{rule_type}|{description}|{destination_port or 'Any'}|{state}"
    args = ["iptables", "-A", APP_FW_CHAIN]
    if zone_iface:
        args.extend(["-i", zone_iface])
    args.extend(["-s", str(source_net), "-d", str(destination_net)])
    if protocol != "ANY":
        args.extend(["-p", protocol.lower()])
    if destination_port:
        args.extend(["--dport", destination_port])
    if state != "ANY":
        args.extend(["-m", "conntrack", "--ctstate", state])
    args.extend(["-m", "comment", "--comment", comment, "-j", target])
    run_cmd(args)


def firewall_rule_specs():
    if not filter_chain_exists(APP_FW_CHAIN):
        return []
    specs = []
    for line in run_cmd(["iptables", "-S", APP_FW_CHAIN]).splitlines():
        if line.startswith(f"-A {APP_FW_CHAIN} "):
            specs.append(shlex.split(line)[2:])
    return specs


def move_firewall_rule(line, direction):
    line_number = int(str(line).strip())
    direction = direction.strip().lower()
    specs = firewall_rule_specs()
    if line_number < 1 or line_number > len(specs):
        raise NetworkError("Rule number is outside the current rule list")
    if direction not in {"up", "down"}:
        raise NetworkError("Direction must be up or down")
    if direction == "up" and line_number == 1:
        return
    if direction == "down" and line_number == len(specs):
        return

    selected = specs[line_number - 1]
    insert_at = line_number - 1 if direction == "up" else line_number + 1
    run_cmd(["iptables", "-D", APP_FW_CHAIN, str(line_number)])
    run_cmd(["iptables", "-I", APP_FW_CHAIN, str(insert_at), *selected])


def delete_firewall_rule(line):
    line_number = int(str(line).strip())
    if line_number < 1:
        raise NetworkError("Rule number must be positive")
    ensure_firewall_chain()
    run_cmd(["iptables", "-D", APP_FW_CHAIN, str(line_number)])
    if not firewall_rule_specs():
        reset_firewall()


def reset_firewall():
    if os.environ.get("PART4_AUTOCONFIG") == "1":
        run_cmd(["python", "/app/init-part3.py"])
        return
    if filter_chain_exists(APP_FW_CHAIN):
        run_cmd(["iptables", "-F", APP_FW_CHAIN])
    while has_forward_jump():
        run_cmd(["iptables", "-D", "FORWARD", "-j", APP_FW_CHAIN])
    if filter_chain_exists(APP_FW_CHAIN):
        run_cmd(["iptables", "-X", APP_FW_CHAIN])


def firewall_rules():
    if not filter_chain_exists(APP_FW_CHAIN):
        return []
    out = run_cmd(["iptables", "-L", APP_FW_CHAIN, "-n", "-v", "--line-numbers"])
    specs = firewall_rule_specs()
    rows = []
    for line in out.splitlines():
        parts = line.split()
        if not parts or not parts[0].isdigit():
            continue
        line_no, packets, byte_count, target, protocol = parts[:5]
        source = parts[8] if len(parts) > 8 else ""
        destination = parts[9] if len(parts) > 9 else ""
        in_iface = parts[6] if len(parts) > 6 else "*"
        action = "ALLOW" if target == "ACCEPT" else "DENY" if target == "DROP" else target
        protocol_label = "ANY" if protocol == "all" else protocol.upper()
        zone = "Any"
        for item in firewall_zones():
            if item["name"] == in_iface:
                zone = item["role"]
                break
        description = ""
        destination_port = "Any"
        state = "ANY"
        rule_type = "Firewall" if zone != "Any" or protocol != "all" else "ACL"
        spec_index = int(line_no) - 1
        if 0 <= spec_index < len(specs):
            spec = specs[spec_index]
            if "--comment" in spec:
                comment = spec[spec.index("--comment") + 1]
                fields = comment.split("|")
                if len(fields) >= 10 and fields[0] == "MOSEC":
                    rule_type = fields[6] if fields[6] in {"ACL", "Firewall"} else rule_type
                    description = fields[7]
                    destination_port = fields[8]
                    state = fields[9]
                elif len(fields) >= 8 and fields[0] == "MOSEC":
                    rule_type = fields[6] if fields[6] in {"ACL", "Firewall"} else rule_type
                    description = fields[7]
                elif len(fields) >= 7 and fields[0] == "MOSEC":
                    description = fields[6]
                elif len(fields) >= 3 and fields[0] in {"TEACHER", "PARTIII"}:
                    part4_teacher = fields[:2] == ["TEACHER", "PARTIV"] and len(fields) >= 4
                    category = fields[2] if part4_teacher else fields[1]
                    rule_type = "ACL" if category == "ACL" else "Firewall"
                    description = fields[-1]
                else:
                    description = comment
            if "--dport" in spec:
                destination_port = spec[spec.index("--dport") + 1]
            if "--dports" in spec:
                destination_port = spec[spec.index("--dports") + 1]
            if "--ctstate" in spec:
                state = spec[spec.index("--ctstate") + 1]
        if rule_type == "ACL":
            zone = "-"
            protocol_label = "-"
            destination_port = "-"
            state = "-"
        rows.append({
            "line": line_no,
            "packets": packets,
            "bytes": byte_count,
            "action": action,
            "source": source,
            "destination": destination,
            "protocol": protocol_label,
            "destination_port": destination_port,
            "state": state,
            "zone": zone,
            "description": description,
            "rule_type": rule_type,
            "raw": line,
        })
    return rows


def reset_router():
    if os.environ.get("PART4_AUTOCONFIG") == "1":
        run_cmd(["/app/init-part2.sh"])
        run_cmd(["python", "/app/init-part3.py"])
        return
    set_ip_forwarding(False)
    reset_firewall()
    disable_nat()
    run_cmd(["ip", "route", "replace", "default", "via", "172.30.255.1"])
    for route in routes():
        if route["deletable"]:
            try:
                delete_static_route(route["destination"], route["gateway"], route["interface"])
            except NetworkError:
                pass
    for role, name in parse_role_interfaces().items():
        run_cmd(["ip", "addr", "flush", "dev", name])
