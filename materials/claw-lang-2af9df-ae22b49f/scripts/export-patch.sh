#!/usr/bin/env bash
set -euo pipefail
base_commit=ae22b49f2a0989cc85bdc1996a541d8308a02c0b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
