#!/usr/bin/env bash
set -euo pipefail
base_commit=3a6a9c882f99dbfe5dec04ee68f78b25a68b3f70
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
