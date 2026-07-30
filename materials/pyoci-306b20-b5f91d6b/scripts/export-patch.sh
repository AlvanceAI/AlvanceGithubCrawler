#!/usr/bin/env bash
set -euo pipefail
base_commit=b5f91d6b0f96aa8d8cb677dfecd187ef6f8b3f0f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
