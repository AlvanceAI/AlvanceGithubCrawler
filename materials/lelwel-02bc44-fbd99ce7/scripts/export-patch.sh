#!/usr/bin/env bash
set -euo pipefail
base_commit=fbd99ce71960489c070620015dd4f8227448262c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
