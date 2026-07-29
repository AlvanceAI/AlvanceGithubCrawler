#!/usr/bin/env bash
set -euo pipefail
base_commit=0d3d06c94bf1f0a61b9f44998100024cb0b53feb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
