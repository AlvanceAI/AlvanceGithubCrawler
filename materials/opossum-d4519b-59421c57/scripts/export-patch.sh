#!/usr/bin/env bash
set -euo pipefail
base_commit=59421c572adf568c9f7dab823801e6618a0759c3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
