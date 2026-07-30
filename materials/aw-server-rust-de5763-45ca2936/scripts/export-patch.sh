#!/usr/bin/env bash
set -euo pipefail
base_commit=45ca293650420916117a3c9a771d8d27c2d37f25
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
