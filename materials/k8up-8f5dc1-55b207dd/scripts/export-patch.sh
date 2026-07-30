#!/usr/bin/env bash
set -euo pipefail
base_commit=55b207dddee83c11d8167e973b6c76f3b1493ee8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
