#!/usr/bin/env bash
set -euo pipefail
base_commit=5f85d3f5474aede69f17f71d3e0a36674b8b8b62
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
