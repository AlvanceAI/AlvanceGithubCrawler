#!/usr/bin/env bash
set -euo pipefail
base_commit=6972ac4261ce7bf5b585da9051606c7b5c0ab82c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
