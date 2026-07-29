#!/usr/bin/env bash
set -euo pipefail
base_commit=bf1a12dd416b17c2294d1b57896928bb2e30a3c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
