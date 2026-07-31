#!/usr/bin/env bash
set -euo pipefail
base_commit=746db5ebf42f87da5d487de444dccc884f9d1c39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
