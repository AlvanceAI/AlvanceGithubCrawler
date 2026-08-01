#!/usr/bin/env bash
set -euo pipefail
base_commit=ff542cbe75ea832df3a989d07c7fdf5214f727fa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
