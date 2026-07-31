#!/usr/bin/env bash
set -euo pipefail
base_commit=c7954df0b0aa67bc0ede525b17dec1caabb954b6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
