#!/usr/bin/env bash
set -euo pipefail
base_commit=0cd148e687aa2b3a01e11b9d8fc16fc6d7a4a72f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
