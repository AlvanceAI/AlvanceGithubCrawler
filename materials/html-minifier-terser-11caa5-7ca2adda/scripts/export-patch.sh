#!/usr/bin/env bash
set -euo pipefail
base_commit=7ca2adda16a10cb0dff5f82d71394ec10eb49ce9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
