#!/usr/bin/env bash
set -euo pipefail
base_commit=f9459026b39c98b1ffa0154308892270eb42587e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
