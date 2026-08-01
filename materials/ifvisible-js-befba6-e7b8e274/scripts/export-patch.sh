#!/usr/bin/env bash
set -euo pipefail
base_commit=e7b8e2743becb691a01bff6b8e55dec0e11c338a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
