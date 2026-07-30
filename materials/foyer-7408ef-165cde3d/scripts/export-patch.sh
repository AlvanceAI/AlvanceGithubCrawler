#!/usr/bin/env bash
set -euo pipefail
base_commit=165cde3d4e638aaf2680384c02f57222b40be128
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
