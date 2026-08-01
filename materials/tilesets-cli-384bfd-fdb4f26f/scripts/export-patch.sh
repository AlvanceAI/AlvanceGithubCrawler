#!/usr/bin/env bash
set -euo pipefail
base_commit=fdb4f26f38c836ed25eec16dea35a9441b0ecd97
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
