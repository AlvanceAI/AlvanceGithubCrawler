#!/usr/bin/env bash
set -euo pipefail
base_commit=d246679c72e1c3d2ef0e610503e1c2f74581978b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
