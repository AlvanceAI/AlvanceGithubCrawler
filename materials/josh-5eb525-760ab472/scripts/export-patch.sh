#!/usr/bin/env bash
set -euo pipefail
base_commit=760ab472170d63a30713bd7ae65cacc06baca69b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
