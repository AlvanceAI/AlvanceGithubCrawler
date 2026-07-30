#!/usr/bin/env bash
set -euo pipefail
base_commit=12304d656a72ff0564075fe990207db5cfd82148
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
