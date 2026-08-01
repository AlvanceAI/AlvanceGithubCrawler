#!/usr/bin/env bash
set -euo pipefail
base_commit=65e0618f1c2d4905418a68fa5d829ae624738e0a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
