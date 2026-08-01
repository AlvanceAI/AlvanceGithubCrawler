#!/usr/bin/env bash
set -euo pipefail
base_commit=daab8c9ef39b24204aa2cccd5e7aa7ab2f149ae8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
