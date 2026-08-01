#!/usr/bin/env bash
set -euo pipefail
base_commit=8b33aa0b7e96f837d10058d29f69b7a9dd61cf77
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
