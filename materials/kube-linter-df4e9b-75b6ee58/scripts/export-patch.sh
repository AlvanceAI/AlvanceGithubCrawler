#!/usr/bin/env bash
set -euo pipefail
base_commit=75b6ee58ac416b4c9579be6e128b651ccee386cb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
