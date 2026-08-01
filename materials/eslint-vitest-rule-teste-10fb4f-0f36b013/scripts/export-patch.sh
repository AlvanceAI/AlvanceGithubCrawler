#!/usr/bin/env bash
set -euo pipefail
base_commit=0f36b013e1cf586f1a35f9544f0cda1ba313aa50
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
