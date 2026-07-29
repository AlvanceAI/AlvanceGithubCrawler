#!/usr/bin/env bash
set -euo pipefail
base_commit=1a3147feea968ff1eef67b0bfb3633cbf29fa681
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
