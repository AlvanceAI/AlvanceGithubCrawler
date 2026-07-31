#!/usr/bin/env bash
set -euo pipefail
base_commit=9199c6cf7b1359a19168eba6b41a56bc4633df18
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
