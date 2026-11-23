#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 scripts/platform_check.py
docker compose down
docker compose up -d --build --wait
python3 scripts/wait-web-entry.py
./scripts/test-part4.sh
