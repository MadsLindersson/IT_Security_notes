#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${STUDENT_CIDR:-}" ]]; then
  ip route del default 2>/dev/null || true
  ip addr flush dev eth0
  ip addr add "${STUDENT_CIDR}" dev eth0
  ip link set eth0 up
  if [[ -n "${STUDENT_GATEWAY:-}" ]]; then
    ip route add default via "${STUDENT_GATEWAY}"
  fi
elif [[ "${MODE:-flat}" == "blank" ]]; then
  ip route del default 2>/dev/null || true
  ip addr flush dev eth0
fi

mkdir -p /etc/mosec
rm -rf /etc/nginx
cp -a /opt/nginx-baseline /etc/nginx
rm -rf /etc/nginx/sites-enabled/* /etc/nginx/conf.d/*
rm -rf /usr/local/share/ca-certificates/*
update-ca-certificates --fresh >/dev/null
mkdir -p /etc/nginx/certs /etc/nginx/private
chmod 700 /etc/nginx/private
cp /opt/part4/default.conf /etc/nginx/conf.d/default.conf
cp /opt/part4/tls.conf.example /etc/nginx/tls.conf.example
rm -f /etc/mosec/server.key /etc/mosec/server.crt
printf '0.0.0.0\n' > /etc/mosec/portal-bind
nginx -t
iptables -F INPUT
iptables -P INPUT ACCEPT
iptables -A INPUT -i lo -m comment --comment "host-loopback" -j ACCEPT
iptables -A INPUT -s 10.10.0.10/32 -p tcp --dport 22 -m comment --comment "host-admin-ssh" -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -m comment --comment "host-other-ssh-deny" -j DROP
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
