#!/usr/bin/env bash
set -euo pipefail
base_commit=9bafe07343742c860ff53bf66075648f8ebb54a5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
