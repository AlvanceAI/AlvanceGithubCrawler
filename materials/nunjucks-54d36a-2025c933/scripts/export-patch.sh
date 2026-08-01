#!/usr/bin/env bash
set -euo pipefail
base_commit=2025c933fba374482ef97122514bb36de6bf9de4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
