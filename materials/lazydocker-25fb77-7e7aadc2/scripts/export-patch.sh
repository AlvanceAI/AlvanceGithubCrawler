#!/usr/bin/env bash
set -euo pipefail
base_commit=7e7aadc2071d58031bf2daafca1fbd4093efc23f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
