#!/usr/bin/env bash
set -euo pipefail
base_commit=14b3336bc973023e82325426adf6d71046ebcf55
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
