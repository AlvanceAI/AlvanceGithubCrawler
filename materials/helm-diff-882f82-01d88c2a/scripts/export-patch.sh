#!/usr/bin/env bash
set -euo pipefail
base_commit=01d88c2a943322246aca885a922f45770793b020
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
