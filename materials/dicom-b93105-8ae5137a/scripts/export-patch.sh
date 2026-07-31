#!/usr/bin/env bash
set -euo pipefail
base_commit=8ae5137aa164e11a1ffb53b10778cba6cd910a87
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
