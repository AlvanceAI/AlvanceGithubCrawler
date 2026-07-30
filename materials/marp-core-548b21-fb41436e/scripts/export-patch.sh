#!/usr/bin/env bash
set -euo pipefail
base_commit=fb41436e1db5b43a9f93d288ed361b2550408a0b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
