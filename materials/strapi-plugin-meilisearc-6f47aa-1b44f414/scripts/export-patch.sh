#!/usr/bin/env bash
set -euo pipefail
base_commit=1b44f414dce789c89d021326717d52d30722190c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
