#!/usr/bin/env bash
set -euo pipefail
base_commit=88eb1affedcd11520d8a20910bd17b604705d48d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
