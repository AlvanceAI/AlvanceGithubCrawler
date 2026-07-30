#!/usr/bin/env bash
set -euo pipefail
base_commit=46f4d6f78b2ddca72a7e2b6c78aa0180c6ce4c41
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
