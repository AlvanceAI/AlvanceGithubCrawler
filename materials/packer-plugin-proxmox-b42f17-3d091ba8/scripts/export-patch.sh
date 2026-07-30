#!/usr/bin/env bash
set -euo pipefail
base_commit=3d091ba837c3cc22959acb1a9902ad3816475626
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
