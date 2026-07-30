#!/usr/bin/env bash
set -euo pipefail
base_commit=686701686f8e367f69a762de9f06fd826ca0d406
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
