#!/usr/bin/env bash
set -euo pipefail
base_commit=a088d3856dc95e79d610394bd532a070a4b814ad
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
