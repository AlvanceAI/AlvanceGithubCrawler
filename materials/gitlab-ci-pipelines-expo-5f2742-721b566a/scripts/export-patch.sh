#!/usr/bin/env bash
set -euo pipefail
base_commit=721b566a8176b61e35d43e57f522df350698df8a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
