#!/usr/bin/env bash
set -euo pipefail
base_commit=38b220c9f8c54f8507ed3f02f2e1aeb8884408d6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
