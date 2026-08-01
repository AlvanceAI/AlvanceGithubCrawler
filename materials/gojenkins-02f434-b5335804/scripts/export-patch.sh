#!/usr/bin/env bash
set -euo pipefail
base_commit=b53358041d6023d4cc7bfff8e26e9e3228e0b45b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
