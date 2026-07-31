#!/usr/bin/env bash
set -euo pipefail
base_commit=83f06df0f64d12e974f5cdd390134c8b80c7365b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
