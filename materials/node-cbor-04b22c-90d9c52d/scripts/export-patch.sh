#!/usr/bin/env bash
set -euo pipefail
base_commit=90d9c52d9abbfddd0e550ba14724ac7f3c28a723
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
