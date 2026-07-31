#!/usr/bin/env bash
set -euo pipefail
base_commit=f90bfac9ad9984354437b83e529f5dd709346413
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
