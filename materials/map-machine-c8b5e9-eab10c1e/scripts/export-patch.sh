#!/usr/bin/env bash
set -euo pipefail
base_commit=eab10c1ec9bcd0a78fa6db75d02e6219fcea562c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
