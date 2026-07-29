#!/usr/bin/env bash
set -euo pipefail
base_commit=7255a6a7dac1bd5eabf20ebd9e5c3aeb5a3d9c81
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
