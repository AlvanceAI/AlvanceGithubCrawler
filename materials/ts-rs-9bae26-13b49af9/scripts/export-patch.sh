#!/usr/bin/env bash
set -euo pipefail
base_commit=13b49af94ecf17596122bde4923aae5e4077bf7f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
