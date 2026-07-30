#!/usr/bin/env bash
set -euo pipefail
base_commit=3179c6e62929294961acbfd9bf8445769716a121
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
