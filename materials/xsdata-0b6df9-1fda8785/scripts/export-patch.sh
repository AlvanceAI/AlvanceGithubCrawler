#!/usr/bin/env bash
set -euo pipefail
base_commit=1fda8785e884fd0ce8da214b9d69d5cbb88b89be
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
