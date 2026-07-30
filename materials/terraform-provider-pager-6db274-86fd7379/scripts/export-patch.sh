#!/usr/bin/env bash
set -euo pipefail
base_commit=86fd7379934b24d3964b161bbda463aa691e78a0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
