#!/usr/bin/env bash
set -euo pipefail
base_commit=ef6379f07ba664f78c22e59776376ea475dbe43f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
