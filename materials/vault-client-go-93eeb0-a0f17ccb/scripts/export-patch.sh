#!/usr/bin/env bash
set -euo pipefail
base_commit=a0f17ccb92501f7b7ad1bf5188b404383f08a45f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
