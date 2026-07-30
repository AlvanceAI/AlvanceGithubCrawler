#!/usr/bin/env bash
set -euo pipefail
base_commit=1575f1854c26d9f8846edba386b94f2b8b063f3f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
