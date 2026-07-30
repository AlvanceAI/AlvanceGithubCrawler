#!/usr/bin/env bash
set -euo pipefail
base_commit=5e7d320fa81713a013f7b1ae7e7af3f8c15ad422
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
