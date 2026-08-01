#!/usr/bin/env bash
set -euo pipefail
base_commit=3306054c2446164bf05650a76d1d090d7e5c4502
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
