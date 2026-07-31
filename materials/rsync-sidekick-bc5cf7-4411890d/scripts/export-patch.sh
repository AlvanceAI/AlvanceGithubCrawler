#!/usr/bin/env bash
set -euo pipefail
base_commit=4411890d0d977d9b141913f674b5d40a84dc419b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
