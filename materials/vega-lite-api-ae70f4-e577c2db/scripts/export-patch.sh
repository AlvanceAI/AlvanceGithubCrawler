#!/usr/bin/env bash
set -euo pipefail
base_commit=e577c2dbd6c48c442a1e3de1ab9d561067ad839a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
