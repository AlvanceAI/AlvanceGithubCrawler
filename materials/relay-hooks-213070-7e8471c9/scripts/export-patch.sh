#!/usr/bin/env bash
set -euo pipefail
base_commit=7e8471c9a83d9ccf5ced3369bc96c3a80cde15b7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
