#!/usr/bin/env bash
set -euo pipefail
base_commit=4a697b17b82a7a4249de61b9c7bd7709e171d79b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
