#!/usr/bin/env bash
set -euo pipefail
base_commit=7d835878343a71575c27bf6a326cbcff35fed5bc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
