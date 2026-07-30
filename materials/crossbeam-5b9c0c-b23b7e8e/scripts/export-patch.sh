#!/usr/bin/env bash
set -euo pipefail
base_commit=b23b7e8eca2efdad9bdc1ceb1aee1207a852c03b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
