#!/usr/bin/env bash
set -euo pipefail
base_commit=64c324b05ada858dd43c927182be0c4266f201c2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
