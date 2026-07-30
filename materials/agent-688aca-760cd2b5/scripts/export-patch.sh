#!/usr/bin/env bash
set -euo pipefail
base_commit=760cd2b5984d29c2d513bb15ca33e995fae45f17
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
