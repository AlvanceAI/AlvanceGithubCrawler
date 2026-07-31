#!/usr/bin/env bash
set -euo pipefail
base_commit=6b193047bf2c5626da5dc5f3a23b58ab9bd3f130
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
