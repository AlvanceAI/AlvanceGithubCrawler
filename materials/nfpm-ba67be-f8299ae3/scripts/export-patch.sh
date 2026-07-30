#!/usr/bin/env bash
set -euo pipefail
base_commit=f8299ae32461dde806229ad90bf68d1992b4d05a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
