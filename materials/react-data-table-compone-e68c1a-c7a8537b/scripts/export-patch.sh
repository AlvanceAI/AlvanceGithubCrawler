#!/usr/bin/env bash
set -euo pipefail
base_commit=c7a8537bb5e3eafda7593e38c4810e891dd27e3c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
