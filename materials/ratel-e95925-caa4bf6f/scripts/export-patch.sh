#!/usr/bin/env bash
set -euo pipefail
base_commit=caa4bf6ff97f5f0b59605f9b8855b39bf6d800f5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
