#!/usr/bin/env bash
set -euo pipefail
base_commit=c4177cab47ae109c848a431756d5d7c0207c05ed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
