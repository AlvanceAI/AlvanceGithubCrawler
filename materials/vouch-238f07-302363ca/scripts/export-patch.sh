#!/usr/bin/env bash
set -euo pipefail
base_commit=302363ca56246e093e9334488399005e05b5b977
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
