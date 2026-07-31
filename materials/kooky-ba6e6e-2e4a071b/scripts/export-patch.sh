#!/usr/bin/env bash
set -euo pipefail
base_commit=2e4a071b0dc47a4a09b42b95cc598e9550a25676
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
