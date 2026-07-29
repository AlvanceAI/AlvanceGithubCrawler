#!/usr/bin/env bash
set -euo pipefail
base_commit=3c6441318ebe95991d0cbc3965de039df3cc8777
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
