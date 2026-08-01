#!/usr/bin/env bash
set -euo pipefail
base_commit=e635dbfcf64dcebb62ffc64e4d56d6c83f779791
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
