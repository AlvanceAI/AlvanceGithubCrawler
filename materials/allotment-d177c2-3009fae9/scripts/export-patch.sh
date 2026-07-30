#!/usr/bin/env bash
set -euo pipefail
base_commit=3009fae979e2f3df04f67b342b8402256ee2d636
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
