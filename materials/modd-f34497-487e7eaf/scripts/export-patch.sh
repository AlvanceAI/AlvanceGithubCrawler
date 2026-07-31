#!/usr/bin/env bash
set -euo pipefail
base_commit=487e7eaf245d36a746a180587062a2f67860a0ee
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
