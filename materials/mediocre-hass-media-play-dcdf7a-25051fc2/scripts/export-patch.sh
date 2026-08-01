#!/usr/bin/env bash
set -euo pipefail
base_commit=25051fc2e46c665cba6d2489de6fa5383137784d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
