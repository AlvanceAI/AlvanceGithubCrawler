#!/usr/bin/env bash
set -euo pipefail
base_commit=a5c147e45ad344155e202e86d2adf4442fa796f6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
