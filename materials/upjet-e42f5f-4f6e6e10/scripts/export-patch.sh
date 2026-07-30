#!/usr/bin/env bash
set -euo pipefail
base_commit=4f6e6e10dff292c7bf0410878741e23a97f5c11e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
