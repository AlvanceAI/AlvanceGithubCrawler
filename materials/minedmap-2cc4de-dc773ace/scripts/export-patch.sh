#!/usr/bin/env bash
set -euo pipefail
base_commit=dc773ace9f3dce1e13e1b187a6b8894f78b72a57
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
