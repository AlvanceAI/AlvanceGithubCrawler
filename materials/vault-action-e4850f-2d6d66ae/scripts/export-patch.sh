#!/usr/bin/env bash
set -euo pipefail
base_commit=2d6d66ae680bad91bac6016e160a63c86a3ffe17
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
