#!/usr/bin/env bash
set -euo pipefail
base_commit=5c428f493ef3059246974bedf9a7d89599994b34
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
