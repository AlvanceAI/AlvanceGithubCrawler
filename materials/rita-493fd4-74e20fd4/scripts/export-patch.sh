#!/usr/bin/env bash
set -euo pipefail
base_commit=74e20fd49a77598f47372e5db1175b6d727ece5e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
