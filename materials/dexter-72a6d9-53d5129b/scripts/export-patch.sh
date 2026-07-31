#!/usr/bin/env bash
set -euo pipefail
base_commit=53d5129bb6b3e077464f592433a3985ccd6c7f12
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
