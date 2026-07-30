#!/usr/bin/env bash
set -euo pipefail
base_commit=f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
