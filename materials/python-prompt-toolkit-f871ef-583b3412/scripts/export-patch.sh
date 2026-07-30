#!/usr/bin/env bash
set -euo pipefail
base_commit=583b3412c792a5cc9f01adde603679f3824a88f3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
