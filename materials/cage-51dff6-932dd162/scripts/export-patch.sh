#!/usr/bin/env bash
set -euo pipefail
base_commit=932dd16284ac2e12218741f81a69b5a0e12414cc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
