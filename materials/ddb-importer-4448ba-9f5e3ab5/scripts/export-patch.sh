#!/usr/bin/env bash
set -euo pipefail
base_commit=9f5e3ab56d76026720917d9bef72caa02b2b0c8b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
