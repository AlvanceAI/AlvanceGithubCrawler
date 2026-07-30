#!/usr/bin/env bash
set -euo pipefail
base_commit=d4aea17cff49886eba4da300b06f019134322f90
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
