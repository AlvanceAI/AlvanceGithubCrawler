#!/usr/bin/env bash
set -euo pipefail
base_commit=29e05a213d1edb2429042d02ced1b29c0522a87a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
