#!/usr/bin/env bash
set -euo pipefail
base_commit=7ec5d8a729e03c30524166d0b5ebc15dbdd3a497
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
