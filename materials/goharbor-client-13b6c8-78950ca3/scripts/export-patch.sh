#!/usr/bin/env bash
set -euo pipefail
base_commit=78950ca3611b7b52b67adf8c3dd3b5adfc92ab5f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
