#!/usr/bin/env bash
set -euo pipefail
base_commit=c628a77d9106f68ce514a6b76137a31f40f6dbcf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
