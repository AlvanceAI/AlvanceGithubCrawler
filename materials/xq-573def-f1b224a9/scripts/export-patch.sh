#!/usr/bin/env bash
set -euo pipefail
base_commit=f1b224a9b3fd54b37ed17253bd784bedb475f558
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
