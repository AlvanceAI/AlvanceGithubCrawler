#!/usr/bin/env bash
set -euo pipefail
base_commit=b00216db479c11cae8e7cfec42a79c29af853898
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
