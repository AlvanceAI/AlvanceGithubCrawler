#!/usr/bin/env bash
set -euo pipefail
base_commit=15cffe632969bd9f5b99a19fa2fee8e55a13ce2f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
