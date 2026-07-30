#!/usr/bin/env bash
set -euo pipefail
base_commit=f04bbb03814677ce70e12920b879c3ce173d793e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
