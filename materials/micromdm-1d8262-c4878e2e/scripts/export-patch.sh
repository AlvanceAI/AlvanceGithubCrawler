#!/usr/bin/env bash
set -euo pipefail
base_commit=c4878e2e378e5d3ce90483dd60bcbad90c7b997f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
