#!/usr/bin/env bash
set -euo pipefail
base_commit=39397a86c99f4403b222a62a5f2c744929a4c3af
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
