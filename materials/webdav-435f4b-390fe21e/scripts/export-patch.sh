#!/usr/bin/env bash
set -euo pipefail
base_commit=390fe21ed9aef0a2017b1d85f5f36ffb960c20d3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
