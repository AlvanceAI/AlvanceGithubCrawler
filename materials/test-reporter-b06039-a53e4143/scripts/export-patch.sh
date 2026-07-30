#!/usr/bin/env bash
set -euo pipefail
base_commit=a53e41438c2381e621dc719a47a57180e30c7075
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
