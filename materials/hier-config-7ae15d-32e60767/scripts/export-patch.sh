#!/usr/bin/env bash
set -euo pipefail
base_commit=32e6076719a5199d38e4217a62a9a93b577965ae
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
