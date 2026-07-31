#!/usr/bin/env bash
set -euo pipefail
base_commit=cacd787baae36bbae2d54d46b53756e4b9504556
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
