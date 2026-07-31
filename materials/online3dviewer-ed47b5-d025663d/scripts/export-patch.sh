#!/usr/bin/env bash
set -euo pipefail
base_commit=d025663dcdd101527e87971d9ae2cf16f02949b4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
