#!/usr/bin/env bash
set -euo pipefail
base_commit=4f8d888b3e888b087caf5bb195d663081db5ee98
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
