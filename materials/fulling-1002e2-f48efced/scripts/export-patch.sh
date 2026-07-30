#!/usr/bin/env bash
set -euo pipefail
base_commit=f48efced082a7de3517816267481c04e058672cb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
