#!/usr/bin/env bash
set -euo pipefail
base_commit=9c02e7116ede87b57ee6189c5dc3c22d48937a3a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
