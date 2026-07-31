#!/usr/bin/env bash
set -euo pipefail
base_commit=432ec85e646ba2978f478bfc8f7b8f8f275964fb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
