#!/usr/bin/env bash
set -euo pipefail
base_commit=3edfce9056124e459a23f683a21433670d47daca
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
