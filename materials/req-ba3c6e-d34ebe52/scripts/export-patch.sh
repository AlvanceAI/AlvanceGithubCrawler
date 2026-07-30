#!/usr/bin/env bash
set -euo pipefail
base_commit=d34ebe528dad44a04ec5aa53fae24622c1c8b58b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
