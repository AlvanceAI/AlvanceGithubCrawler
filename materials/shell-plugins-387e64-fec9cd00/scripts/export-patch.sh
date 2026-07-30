#!/usr/bin/env bash
set -euo pipefail
base_commit=fec9cd00b7eea740995e93e457105eea4ff149d7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
