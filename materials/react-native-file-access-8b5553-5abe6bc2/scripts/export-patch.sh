#!/usr/bin/env bash
set -euo pipefail
base_commit=5abe6bc24581a12f173f745226e4afe73e482d5d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
