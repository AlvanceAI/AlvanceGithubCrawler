#!/usr/bin/env bash
set -euo pipefail
base_commit=857a528af6418dcb67b1d9d4fae1100dcd530fa7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
