#!/usr/bin/env bash
set -euo pipefail
base_commit=cd53dae9985c16c49172ad0583fc2e4e2fe223dc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
