#!/usr/bin/env bash
set -euo pipefail
base_commit=4eea7c6fae180a8a2eed45c3f6acd0d9256522b1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
