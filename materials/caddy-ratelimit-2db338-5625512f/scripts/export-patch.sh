#!/usr/bin/env bash
set -euo pipefail
base_commit=5625512f24f6f59d6f64fb3aafe5eecff0b286db
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
