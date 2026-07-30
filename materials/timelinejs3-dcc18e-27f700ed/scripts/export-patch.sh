#!/usr/bin/env bash
set -euo pipefail
base_commit=27f700ed365b675c6e38201130fc141e43f31f26
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
