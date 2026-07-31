#!/usr/bin/env bash
set -euo pipefail
base_commit=453ba51a619a3082302eb507367a31e4c785c331
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
