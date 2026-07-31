#!/usr/bin/env bash
set -euo pipefail
base_commit=c877f5c19b141e25c089d993b4cc584e669b6e39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
