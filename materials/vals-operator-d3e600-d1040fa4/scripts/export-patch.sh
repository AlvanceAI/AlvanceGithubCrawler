#!/usr/bin/env bash
set -euo pipefail
base_commit=d1040fa4b9150f84401a9995226188952927a34f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
