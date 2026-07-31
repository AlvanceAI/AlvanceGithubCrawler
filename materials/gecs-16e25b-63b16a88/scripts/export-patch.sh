#!/usr/bin/env bash
set -euo pipefail
base_commit=63b16a8894604f2e20d0ab5efdf6a03e546736bd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
