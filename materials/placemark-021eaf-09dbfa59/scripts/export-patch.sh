#!/usr/bin/env bash
set -euo pipefail
base_commit=09dbfa59704aa7b7f2836604d06c6fb508875c4f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
