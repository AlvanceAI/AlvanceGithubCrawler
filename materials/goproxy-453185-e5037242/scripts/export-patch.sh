#!/usr/bin/env bash
set -euo pipefail
base_commit=e503724238386713152b7759d1a9fb804e09248e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
