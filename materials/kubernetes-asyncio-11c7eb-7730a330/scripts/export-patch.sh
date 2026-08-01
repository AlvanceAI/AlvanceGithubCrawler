#!/usr/bin/env bash
set -euo pipefail
base_commit=7730a330a5467a7b6c591099bc4465a9db219258
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
