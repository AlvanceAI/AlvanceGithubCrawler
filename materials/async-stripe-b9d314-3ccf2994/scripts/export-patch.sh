#!/usr/bin/env bash
set -euo pipefail
base_commit=3ccf29941c8160711636e7b94bd64aa473d57247
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
