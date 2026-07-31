#!/usr/bin/env bash
set -euo pipefail
base_commit=df52e3c32c66522fa41b9e00231f4c42b874b192
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
