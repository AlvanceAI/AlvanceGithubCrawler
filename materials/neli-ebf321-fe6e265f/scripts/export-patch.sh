#!/usr/bin/env bash
set -euo pipefail
base_commit=fe6e265fcf2ef08614c37c94ea178b899890f574
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
