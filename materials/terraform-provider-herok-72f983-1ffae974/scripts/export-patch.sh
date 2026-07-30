#!/usr/bin/env bash
set -euo pipefail
base_commit=1ffae9740c16ef9b79d27791bf51fc86f2fb08a9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
