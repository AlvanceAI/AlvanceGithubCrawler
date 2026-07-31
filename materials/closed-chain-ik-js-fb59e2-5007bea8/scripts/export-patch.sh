#!/usr/bin/env bash
set -euo pipefail
base_commit=5007bea806e6e03f4eb58f1246e75695a3d4ba76
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
