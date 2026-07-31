#!/usr/bin/env bash
set -euo pipefail
base_commit=b70dea3cc72a7e8f941133b0f486aa1840e3f927
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
