#!/usr/bin/env bash
set -euo pipefail
base_commit=bc87592449bdd43312b363753c077dcd8cb05b30
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
