#!/usr/bin/env bash
set -euo pipefail
base_commit=2f5aaecc2c5f2aa0d64a77d12f8b5945d63928a7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
