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

exec sleep infinity
