#!/usr/bin/env bash
set -euo pipefail
base_commit=83be9ddcf82e8a90ea50a9d54c1ebfc3e22ace16
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
