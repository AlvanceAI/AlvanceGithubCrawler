#!/usr/bin/env bash
set -euo pipefail
base_commit=9f51d9b3769679cf58b8618cbaf10a9eb7e7df30
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
