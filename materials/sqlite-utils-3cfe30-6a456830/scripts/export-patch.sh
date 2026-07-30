#!/usr/bin/env bash
set -euo pipefail
base_commit=6a456830ca33eb5edaa634a9b0febe5d71bea2be
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
