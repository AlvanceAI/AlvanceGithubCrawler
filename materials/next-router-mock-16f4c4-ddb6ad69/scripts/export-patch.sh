#!/usr/bin/env bash
set -euo pipefail
base_commit=ddb6ad690f0e236a5d71a2ea9aa22564c4751fae
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
