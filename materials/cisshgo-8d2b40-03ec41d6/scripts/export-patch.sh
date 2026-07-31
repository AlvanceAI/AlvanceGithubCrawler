#!/usr/bin/env bash
set -euo pipefail
base_commit=03ec41d603010333b25f378add32dc5a19578608
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
