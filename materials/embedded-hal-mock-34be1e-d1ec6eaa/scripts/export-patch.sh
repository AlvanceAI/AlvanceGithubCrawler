#!/usr/bin/env bash
set -euo pipefail
base_commit=d1ec6eaab93f029d433881394528d7232f678310
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
