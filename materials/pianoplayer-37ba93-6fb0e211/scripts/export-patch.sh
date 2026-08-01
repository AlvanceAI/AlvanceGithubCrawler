#!/usr/bin/env bash
set -euo pipefail
base_commit=6fb0e2114d7b21f75c0be5208172e1243a57323e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
