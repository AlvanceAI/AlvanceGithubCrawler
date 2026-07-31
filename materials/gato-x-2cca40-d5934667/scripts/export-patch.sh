#!/usr/bin/env bash
set -euo pipefail
base_commit=d5934667f448004aeb664f19725eb2f4ac267839
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
