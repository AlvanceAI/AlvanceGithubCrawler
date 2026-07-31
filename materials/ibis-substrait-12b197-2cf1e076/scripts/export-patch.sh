#!/usr/bin/env bash
set -euo pipefail
base_commit=2cf1e0769ea93859be832cfa1554b4351e0f235f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
