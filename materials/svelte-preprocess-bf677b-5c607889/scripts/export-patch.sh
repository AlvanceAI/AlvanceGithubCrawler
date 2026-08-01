#!/usr/bin/env bash
set -euo pipefail
base_commit=5c607889f1b09e48fce8a400d16a123c6c25ef56
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
