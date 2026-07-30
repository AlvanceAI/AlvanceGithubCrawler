#!/usr/bin/env bash
set -euo pipefail
base_commit=77d9741d10502723e9dd3aeae2f6c540b0893456
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
