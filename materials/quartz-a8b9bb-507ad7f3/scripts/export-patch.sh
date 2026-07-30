#!/usr/bin/env bash
set -euo pipefail
base_commit=507ad7f3d4601d83482f61930fccf1c77f42a072
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
