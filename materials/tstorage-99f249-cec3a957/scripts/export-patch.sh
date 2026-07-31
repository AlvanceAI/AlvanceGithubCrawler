#!/usr/bin/env bash
set -euo pipefail
base_commit=cec3a9574c70a6069225b5bce2993bfa9adf00f8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
