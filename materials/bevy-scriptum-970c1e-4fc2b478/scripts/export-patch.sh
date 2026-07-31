#!/usr/bin/env bash
set -euo pipefail
base_commit=4fc2b47834a6314967367f5b4e6b8e5e85d93690
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
