#!/usr/bin/env bash
set -euo pipefail
base_commit=ac8c3872509a56fb4bd9c1ef853de01f391c058b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
