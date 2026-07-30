#!/usr/bin/env bash
set -euo pipefail
base_commit=23f0dd8b80827ae784fd1d787fc8e9ecdd50cbeb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
