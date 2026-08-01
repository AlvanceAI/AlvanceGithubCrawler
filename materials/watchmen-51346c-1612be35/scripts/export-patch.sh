#!/usr/bin/env bash
set -euo pipefail
base_commit=1612be3537fdccaa477cedae38acb2f61dffa935
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
