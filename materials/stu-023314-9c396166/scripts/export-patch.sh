#!/usr/bin/env bash
set -euo pipefail
base_commit=9c3961660ef0c46b7b7f821b48bd22b8b349b8b6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
