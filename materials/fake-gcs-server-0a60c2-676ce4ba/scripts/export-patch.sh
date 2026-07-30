#!/usr/bin/env bash
set -euo pipefail
base_commit=676ce4ba764b2d90ab139e3d6e580cd0c55ca562
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
