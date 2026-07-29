#!/usr/bin/env bash
set -euo pipefail
base_commit=e7d95d494cebc66fd220198ea2eb2cf94a8bb5fe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
