#!/usr/bin/env bash
set -euo pipefail
base_commit=3297261f7a511654d0fe9d10b272ec30fdafca55
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
