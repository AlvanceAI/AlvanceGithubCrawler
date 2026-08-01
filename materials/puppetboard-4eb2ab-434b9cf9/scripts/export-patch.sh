#!/usr/bin/env bash
set -euo pipefail
base_commit=434b9cf9e3e7477b09a88886d073c520dc610155
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
