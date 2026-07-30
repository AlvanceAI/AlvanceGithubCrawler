#!/usr/bin/env bash
set -euo pipefail
base_commit=8a3c6e200b9548fb0bc22d9cd7470bb55b3667dc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
