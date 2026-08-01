#!/usr/bin/env bash
set -euo pipefail
base_commit=1f34ba106ecc597564a4a75406d47689d8eb01b1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
