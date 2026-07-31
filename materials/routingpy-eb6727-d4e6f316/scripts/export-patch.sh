#!/usr/bin/env bash
set -euo pipefail
base_commit=d4e6f316f28e4d9df9bff251198ee6b6b4418132
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
