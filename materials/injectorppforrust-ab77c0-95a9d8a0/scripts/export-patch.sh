#!/usr/bin/env bash
set -euo pipefail
base_commit=95a9d8a031abe63ee0b8f96b70feb2ff80602c50
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
