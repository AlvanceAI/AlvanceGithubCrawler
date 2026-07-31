#!/usr/bin/env bash
set -euo pipefail
base_commit=152a90b67e497fb2dcc44da5c5d0e6938cfe22f1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
