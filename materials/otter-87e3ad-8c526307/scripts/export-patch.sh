#!/usr/bin/env bash
set -euo pipefail
base_commit=8c526307556486ea0337280a4211135720bc29cc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
