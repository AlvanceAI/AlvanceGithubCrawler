#!/usr/bin/env bash
set -euo pipefail
base_commit=b5c27d9477bc2aa1a8fbb7a2332c7ae8b6aadfcc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
