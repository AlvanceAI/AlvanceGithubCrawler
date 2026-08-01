#!/usr/bin/env bash
set -euo pipefail
base_commit=9bb21b12ca04f1052b4ebe43438d5ce1991193b2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
