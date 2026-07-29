#!/usr/bin/env bash
set -euo pipefail
base_commit=465b34d38c85cc0eaa9ff020518cbc0aa0303d15
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
