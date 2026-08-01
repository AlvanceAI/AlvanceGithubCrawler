#!/usr/bin/env bash
set -euo pipefail
base_commit=cde2d1b392a4ceb9b60a926218ed845939d85c07
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
