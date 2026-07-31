#!/usr/bin/env bash
set -euo pipefail
base_commit=1b8dc0b1af89872bb2bf081f26f536ac95efb9d7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
