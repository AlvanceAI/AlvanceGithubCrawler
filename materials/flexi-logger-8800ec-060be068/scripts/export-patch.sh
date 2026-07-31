#!/usr/bin/env bash
set -euo pipefail
base_commit=060be0689a88a42f98c1bd88b9b99ad80ace2608
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
