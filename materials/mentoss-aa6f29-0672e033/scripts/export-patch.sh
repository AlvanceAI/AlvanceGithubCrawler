#!/usr/bin/env bash
set -euo pipefail
base_commit=0672e0336c9235bf07a205381496df301dbbe4ad
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
