#!/usr/bin/env bash
set -euo pipefail
base_commit=f4c2e3bfb9cfff0a430c513ad2198634412e22a1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
