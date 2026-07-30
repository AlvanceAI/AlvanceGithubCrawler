#!/usr/bin/env bash
set -euo pipefail
base_commit=f3299aac1ff4e1c7278bbbde80cde66f279203bc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
