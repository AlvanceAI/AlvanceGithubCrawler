#!/usr/bin/env bash
set -euo pipefail
base_commit=720065d36f434c616017441aa8f2069e621b5e44
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
