#!/usr/bin/env bash
set -euo pipefail
base_commit=87b41d415406341588f95ca77ba3e734c3276e6a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
