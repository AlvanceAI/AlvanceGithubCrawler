#!/usr/bin/env bash
set -euo pipefail
base_commit=0eb287f5a67fafc364a2922e0b70e6ca636c6871
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
