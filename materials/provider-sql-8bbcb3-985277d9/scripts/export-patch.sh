#!/usr/bin/env bash
set -euo pipefail
base_commit=985277d98fb9f0ce663c9ca5766c611032e069b0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
