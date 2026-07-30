#!/usr/bin/env bash
set -euo pipefail
base_commit=151f96471ebb8bf98ab6d867fb567ae63cba9c9f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
