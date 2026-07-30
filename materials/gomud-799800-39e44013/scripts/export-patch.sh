#!/usr/bin/env bash
set -euo pipefail
base_commit=39e440131769545b61e37bdb3ea89e64ed424871
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
