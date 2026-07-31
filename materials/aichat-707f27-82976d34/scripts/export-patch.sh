#!/usr/bin/env bash
set -euo pipefail
base_commit=82976d349ad97ac9aae0655ad631dace5e2a6385
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
