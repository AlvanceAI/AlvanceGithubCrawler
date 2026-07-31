#!/usr/bin/env bash
set -euo pipefail
base_commit=ee421c326460c57ed61374560c20aa6bc9424186
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
