#!/usr/bin/env bash
set -euo pipefail
base_commit=2a222de65ed15832d4d4adfbbce564539b80115f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
