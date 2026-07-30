#!/usr/bin/env bash
set -euo pipefail
base_commit=2af7645942d431a6d02ca5c13a519e6ca6e70f0f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
