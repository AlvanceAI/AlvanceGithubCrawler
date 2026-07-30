#!/usr/bin/env bash
set -euo pipefail
base_commit=e9bbb01fe7c5b96790f7a60de9c2ee60138a9a6c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
