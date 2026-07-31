#!/usr/bin/env bash
set -euo pipefail
base_commit=38f98617e2e3b2aafeddc147eda58c8830733548
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
