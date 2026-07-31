#!/usr/bin/env bash
set -euo pipefail
base_commit=3453b34e8dcf0482c650f917e60d43ed944a71e2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
