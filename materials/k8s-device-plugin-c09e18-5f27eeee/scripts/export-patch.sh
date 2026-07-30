#!/usr/bin/env bash
set -euo pipefail
base_commit=5f27eeeee7eb7f7a4c0581aa10abeda7e4604ed2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
