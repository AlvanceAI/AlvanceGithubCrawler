#!/usr/bin/env bash
set -euo pipefail
base_commit=24d0731f3fc83d239ddd6b54bb09e8e9ebea5ff9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
