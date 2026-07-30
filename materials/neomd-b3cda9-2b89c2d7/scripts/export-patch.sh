#!/usr/bin/env bash
set -euo pipefail
base_commit=2b89c2d75f4d992029499fde69f55aa5219fda83
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
