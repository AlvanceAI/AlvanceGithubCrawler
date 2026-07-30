#!/usr/bin/env bash
set -euo pipefail
base_commit=8dda19e8e4613e014f0b12f3e624fdff5e5f23b3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
