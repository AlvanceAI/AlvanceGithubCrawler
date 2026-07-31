#!/usr/bin/env bash
set -euo pipefail
base_commit=8f832421115bd40e7f298ef018079f45fd58c77f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
