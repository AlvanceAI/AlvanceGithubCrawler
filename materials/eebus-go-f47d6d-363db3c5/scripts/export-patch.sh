#!/usr/bin/env bash
set -euo pipefail
base_commit=363db3c5c262a4bdb902fa42b602eb9facc1a4a9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
