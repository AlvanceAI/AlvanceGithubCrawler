#!/usr/bin/env bash
set -euo pipefail
base_commit=6e946dd09b43cf6ad25105bb7e07c72a0491650c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
