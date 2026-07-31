#!/usr/bin/env bash
set -euo pipefail
base_commit=a1a0d7fcf406d308392bb653ed6d243d017a3d1c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
