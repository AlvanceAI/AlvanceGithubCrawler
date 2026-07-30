#!/usr/bin/env bash
set -euo pipefail
base_commit=c7c1d75bf231295ae374c4d0cae1b56bbdd5ee13
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
