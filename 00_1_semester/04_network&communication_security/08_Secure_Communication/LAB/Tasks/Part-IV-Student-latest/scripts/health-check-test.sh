#!/usr/bin/env bash
# Check an already-running, unsolved Part IV lab. Never start/reset containers.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

case "${1:-}" in
  --help|-h)
    echo "Usage: $0 [--read-only]"
    echo "Checks the running baseline and runs both existing validation suites."
    echo "--read-only skips the full suite's temporary listener probes."
    echo "Does not start, recreate or reset containers. Exit 0 = PASS; 1 = FAIL."
    exit 0 ;;
  --read-only|'') ;;
  *) echo "Unknown argument: $1 (use --help)" >&2; exit 1 ;;
esac
if [[ $# -gt 1 ]]; then
  echo "Too many arguments (use --help)" >&2
  exit 1
fi

passed=0
failed=0
log=$(mktemp)
trap 'rm -f "$log"' EXIT

check() {
  local label=$1
  shift
  printf '\n[TEST] %s\n' "$label"
  if "$@" >"$log" 2>&1; then
    printf '[PASS] %s\n' "$label"
    passed=$((passed + 1))
    return 0
  else
    printf '[FAIL] %s\n' "$label"
    cat "$log"
    failed=$((failed + 1))
    return 1
  fi
}

summary() {
  printf '\nResult: %s passed, %s failed\n' "$passed" "$failed"
  if [[ $failed -eq 0 ]]; then
    echo 'PASS: Part IV baseline health checks completed.'
  else
    echo 'FAIL: Review the failed checks above.'
  fi
}

running_containers() {
  python3 - <<'PY'
import json
import subprocess
names = ['router', 'router-gui', 'admin', 'employee', 'server', 'guest', 'printer']
containers = json.loads(subprocess.check_output(['docker', 'inspect', *names], text=True))
for container in containers:
    state = container['State']
    assert state['Running'], f"{container['Name']} is not running"
    if 'Health' in state:
        assert state['Health']['Status'] == 'healthy', f"{container['Name']}: {state['Health']}"
PY
}

backend_configuration() {
  python3 - <<'PY'
import json
import subprocess
container = json.loads(subprocess.check_output(['docker', 'inspect', 'server'], text=True))[0]
healthcheck = container['Config']['Healthcheck']['Test']
assert 'http://localhost:8080 ' in healthcheck[-1], healthcheck
listeners = subprocess.check_output(['docker', 'exec', 'server', 'ss', '-lnt'], text=True)
assert '0.0.0.0:8080 ' in listeners, listeners
nginx = subprocess.check_output(['docker', 'exec', 'server', 'nginx', '-T'], text=True)
active = '\n'.join(line.split('#', 1)[0] for line in nginx.splitlines())
assert 'proxy_pass http://127.0.0.1:8080;' in active, 'Incorrect Nginx upstream'
PY
}

http_ok() {
  local status
  status=$(curl --noproxy '*' --max-time 8 -sS -L -o /dev/null -w '%{http_code}' "$1") || return 1
  [[ "$status" == 200 ]] || { echo "Expected HTTP 200, got $status"; return 1; }
}

old_backend_closed() {
  # Only connection refusal counts as success; a broken docker exec must fail.
  docker exec server python3 -c '
import socket
try:
    with socket.create_connection(("127.0.0.1", 8082), timeout=3):
        raise SystemExit("Unexpected listener on old backend port 8082")
except ConnectionRefusedError:
    pass
'
}

printf 'MoSec Part IV baseline health check\n'
echo 'Run against the unsolved HTTP baseline. Completed student configurations may fail.'
echo 'Containers will not be recreated. The full suite uses temporary listeners.'

# Stop before accessing identically named containers owned by another checkout.
if ! check 'Docker platform, Compose configuration and checkout ownership' python3 scripts/platform_check.py; then
  summary
  exit 1
fi
if ! check 'All seven containers running; configured healthchecks healthy' running_containers; then
  echo 'Start the intended baseline first. Warning: make start discards container-local work.'
  summary
  exit 1
fi

check 'Server healthcheck, wildcard listener and Nginx upstream use 8080' backend_configuration || true
check 'Python backend responds inside Server on 8080' docker exec server curl --noproxy '*' --max-time 5 -fsS http://127.0.0.1:8080/ || true
check 'Old Server backend port 8082 refuses connections (expected)' old_backend_closed || true
check 'Host Staff Portal on 8080' http_ok http://localhost:8080/login || true
check 'Host HTTP alias on 80' http_ok http://localhost:80/login || true
check 'Host Router GUI on 8082 (follows login redirect)' http_ok http://localhost:8082/firewall || true
check 'Read-only suite: authentication, actual backend isolation, SSH, Internet and inactive TLS' ./scripts/test-part4.sh --read-only || true
if [[ "${1:-}" != --read-only ]]; then
  check 'Full baseline suite including temporary traffic probes' ./scripts/test-part4.sh || true
else
  echo '[SKIP] Full suite (--read-only selected)'
fi
summary
[[ $failed -eq 0 ]]
