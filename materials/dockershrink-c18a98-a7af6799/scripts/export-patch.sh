#!/usr/bin/env bash
set -euo pipefail
base_commit=a7af6799f2b423efe0499535b7cc388b24184d37
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
