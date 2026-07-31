#!/usr/bin/env bash
set -euo pipefail
base_commit=03a9e6da871c4da67919ee710f755ca9aadc1b36
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
