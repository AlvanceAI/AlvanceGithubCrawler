#!/usr/bin/env bash
set -euo pipefail
base_commit=fc0098898946fd681e9f9758c4512cfe17f32b52
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
