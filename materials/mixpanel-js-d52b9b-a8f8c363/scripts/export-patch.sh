#!/usr/bin/env bash
set -euo pipefail
base_commit=a8f8c363ea3c54d6935ba152230ed8fa157a24f4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
