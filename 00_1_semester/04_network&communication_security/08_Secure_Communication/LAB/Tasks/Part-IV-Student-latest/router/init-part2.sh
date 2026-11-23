#!/usr/bin/env bash
set -euo pipefail

wan="${WAN_INTERFACE:-eth0}"

ip route replace default via 172.30.255.1 dev "$wan" 2>/dev/null || true

# Fail closed while rebuilding the network and policy.
sysctl -w net.ipv4.ip_forward=0 >/dev/null
iptables -P FORWARD DROP
python /app/validate-links.py
for pair in eth1:10.10.0.1 eth2:10.10.0.33 eth3:10.10.0.65 eth4:10.10.0.97 eth5:10.10.0.129; do
  iface="${pair%%:*}"
  ip addr flush dev "$iface"
  ip link set "$iface" up
  ip addr add "${pair#*:}/27" dev "$iface"
done

iptables -D FORWARD -j MOSEC_FORWARD 2>/dev/null || true
iptables -F MOSEC_FORWARD 2>/dev/null || true
iptables -X MOSEC_FORWARD 2>/dev/null || true
iptables -D FORWARD -j MOSEC_ACL 2>/dev/null || true
iptables -F MOSEC_ACL 2>/dev/null || true
iptables -X MOSEC_ACL 2>/dev/null || true

iptables -t nat -N MOSEC_NAT 2>/dev/null || true
iptables -t nat -F MOSEC_NAT
while iptables -t nat -C POSTROUTING -j MOSEC_NAT 2>/dev/null; do
  iptables -t nat -D POSTROUTING -j MOSEC_NAT
done
iptables -t nat -A POSTROUTING -j MOSEC_NAT
iptables -t nat -A MOSEC_NAT -o "$wan" -j MASQUERADE
