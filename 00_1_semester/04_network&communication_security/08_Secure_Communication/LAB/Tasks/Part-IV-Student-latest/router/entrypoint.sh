#!/usr/bin/env bash
set -euo pipefail

python /app/validate-links.py

ip route replace default via 172.30.255.1 dev "${WAN_INTERFACE:-eth0}" 2>/dev/null || true

for iface in ${LAN_INTERFACES:-}; do
  ip route del default dev "$iface" 2>/dev/null || true
  ip addr flush dev "$iface" 2>/dev/null || true
  ip link set "$iface" up 2>/dev/null || true
done

iptables -t nat -D POSTROUTING -j MOSEC_NAT 2>/dev/null || true
iptables -t nat -F MOSEC_NAT 2>/dev/null || true
iptables -t nat -X MOSEC_NAT 2>/dev/null || true
iptables -D FORWARD -j MOSEC_FORWARD 2>/dev/null || true
iptables -F MOSEC_FORWARD 2>/dev/null || true
iptables -X MOSEC_FORWARD 2>/dev/null || true
iptables -D FORWARD -j MOSEC_ACL 2>/dev/null || true
iptables -F MOSEC_ACL 2>/dev/null || true
iptables -X MOSEC_ACL 2>/dev/null || true

if [[ "${PART2_AUTOCONFIG:-0}" == "1" ]]; then
  /app/init-part2.sh
else
  sysctl -w net.ipv4.ip_forward=0 >/dev/null
fi

if [[ "${PART4_AUTOCONFIG:-0}" == "1" ]]; then
  python /app/init-part3.py
  # Refresh peers after a router-only recreation changes this container's MAC.
  for pair in eth1:10.10.0.1 eth2:10.10.0.33 eth3:10.10.0.65 eth4:10.10.0.97 eth5:10.10.0.129; do
    arping -U -c 1 -I "${pair%%:*}" "${pair#*:}"
  done
fi

exec flask --app app run --host=0.0.0.0 --port=8080
