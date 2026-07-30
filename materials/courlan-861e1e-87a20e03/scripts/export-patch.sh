#!/usr/bin/env bash
set -euo pipefail
base_commit=87a20e03f7456ce12278048f3281765f9ca9710c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
