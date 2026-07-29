#!/usr/bin/env bash
set -euo pipefail
base_commit=27253f52c336e71fcac8441845ab0ff6e418ce60
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
