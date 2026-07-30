#!/usr/bin/env bash
set -euo pipefail
base_commit=b8a45d088e922b6abcd87c4eb1b7237919e9d3d2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
