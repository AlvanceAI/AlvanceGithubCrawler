#!/usr/bin/env bash
set -euo pipefail
base_commit=cac2555e44cdd1e3d9eb187e3b29f1ebb907bfab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
