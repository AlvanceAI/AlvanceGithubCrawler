#!/usr/bin/env bash
set -euo pipefail
base_commit=69d9647389f7e47ce7329ab52949d335eef4a41e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
