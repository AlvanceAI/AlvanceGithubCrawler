#!/usr/bin/env bash
set -euo pipefail
base_commit=79c9289d50286492420e1ab3954aa4c15fdeedd7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
