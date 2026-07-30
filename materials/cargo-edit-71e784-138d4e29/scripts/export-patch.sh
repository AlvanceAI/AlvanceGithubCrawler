#!/usr/bin/env bash
set -euo pipefail
base_commit=138d4e2948ddcbf249c31c584b02e1b161a86221
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
