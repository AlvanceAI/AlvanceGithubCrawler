#!/usr/bin/env bash
set -euo pipefail
base_commit=e597f23ecfb88b82f706c5f0cac9d4577c2af262
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
