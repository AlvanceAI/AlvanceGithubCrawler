#!/usr/bin/env bash
set -euo pipefail
base_commit=bd415af2d29bc424bdbd5699af0b472242cc529f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
