#!/usr/bin/env bash
set -euo pipefail
base_commit=a89f789e126741a1814109b6ac15fff7c143a077
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
