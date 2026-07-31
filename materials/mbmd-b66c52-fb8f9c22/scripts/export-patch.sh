#!/usr/bin/env bash
set -euo pipefail
base_commit=fb8f9c22f1210740ac89064fb55610613bba3f78
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
