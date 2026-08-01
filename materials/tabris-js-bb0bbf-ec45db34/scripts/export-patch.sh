#!/usr/bin/env bash
set -euo pipefail
base_commit=ec45db341b137e964bfd69aa6a1c49e6dd0780ea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
