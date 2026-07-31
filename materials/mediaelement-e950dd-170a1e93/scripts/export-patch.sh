#!/usr/bin/env bash
set -euo pipefail
base_commit=170a1e93594e45a03f8c8ece907f22269eec1e9a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
