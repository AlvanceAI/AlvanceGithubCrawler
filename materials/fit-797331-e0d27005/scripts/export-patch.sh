#!/usr/bin/env bash
set -euo pipefail
base_commit=e0d27005ab71b74f34a64f9fab836d375fac875b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
