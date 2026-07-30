#!/usr/bin/env bash
set -euo pipefail
base_commit=c05f20798917d8df814d1154aea3135a53f7f944
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
