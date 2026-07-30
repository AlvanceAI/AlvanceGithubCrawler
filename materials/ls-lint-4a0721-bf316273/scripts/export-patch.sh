#!/usr/bin/env bash
set -euo pipefail
base_commit=bf316273fc386ba5219c8a30c5ea2652b8f4c127
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
