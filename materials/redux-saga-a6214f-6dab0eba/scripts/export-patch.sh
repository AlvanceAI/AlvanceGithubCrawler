#!/usr/bin/env bash
set -euo pipefail
base_commit=6dab0ebadf05a54dcda626f1caa9d8dc3279a845
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
