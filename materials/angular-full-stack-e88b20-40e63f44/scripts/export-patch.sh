#!/usr/bin/env bash
set -euo pipefail
base_commit=40e63f44affcf0d0368429768a085b90b3c5e23e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
