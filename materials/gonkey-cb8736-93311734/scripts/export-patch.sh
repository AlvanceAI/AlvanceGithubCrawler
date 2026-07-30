#!/usr/bin/env bash
set -euo pipefail
base_commit=933117343a864cedf7f7cdecf2b78c379d02908a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
