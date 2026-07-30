#!/usr/bin/env bash
set -euo pipefail
base_commit=14c1018f2b8e8af03b11d2e31a76b8b6835dc977
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
