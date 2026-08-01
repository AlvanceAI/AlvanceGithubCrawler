#!/usr/bin/env bash
set -euo pipefail
base_commit=c487a29895dcfcb5b672247e646426a56e2051c1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
