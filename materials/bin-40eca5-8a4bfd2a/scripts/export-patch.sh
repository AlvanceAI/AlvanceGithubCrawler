#!/usr/bin/env bash
set -euo pipefail
base_commit=8a4bfd2a595ae55db07919bd79bef0e239596dd1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
