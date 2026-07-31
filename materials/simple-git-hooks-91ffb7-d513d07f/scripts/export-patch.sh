#!/usr/bin/env bash
set -euo pipefail
base_commit=d513d07f2cde3f26e68605e8336ece3bb524f329
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
