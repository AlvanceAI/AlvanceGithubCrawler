#!/usr/bin/env bash
set -euo pipefail
base_commit=cd2ecb8d008618f0bbab761898a823bf5999aeb8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
