#!/usr/bin/env bash
set -euo pipefail
base_commit=a35cb309d2ac603d3ad62e556c36725c31c2f907
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
