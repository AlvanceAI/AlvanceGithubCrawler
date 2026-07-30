#!/usr/bin/env bash
set -euo pipefail
base_commit=4a2a8a71b45cb3c1c9dd37f6cdfa314009c37ef1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
