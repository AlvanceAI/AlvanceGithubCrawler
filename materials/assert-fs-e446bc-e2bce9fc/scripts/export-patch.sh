#!/usr/bin/env bash
set -euo pipefail
base_commit=e2bce9fcc4268a92f30fed0218e8695865dafa15
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
