#!/usr/bin/env bash
set -euo pipefail
base_commit=8fcb21b61d157d2688ebfb8949f1c806276e6919
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
