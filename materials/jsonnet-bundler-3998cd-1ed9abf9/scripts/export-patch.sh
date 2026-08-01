#!/usr/bin/env bash
set -euo pipefail
base_commit=1ed9abf9464091454c4a4248e7cb2380b60fb074
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
