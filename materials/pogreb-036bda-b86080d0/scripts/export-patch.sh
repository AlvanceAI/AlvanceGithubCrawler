#!/usr/bin/env bash
set -euo pipefail
base_commit=b86080d06267f8d12067cd432ffd9e5b6916d354
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
