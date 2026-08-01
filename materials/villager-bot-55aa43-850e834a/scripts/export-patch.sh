#!/usr/bin/env bash
set -euo pipefail
base_commit=850e834a0654339a3c787311c177aa4b1d15f546
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
