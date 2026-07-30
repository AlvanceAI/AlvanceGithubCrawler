#!/usr/bin/env bash
set -euo pipefail
base_commit=b618197654e244702af26a74b01d50d5764a3b4d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
