#!/usr/bin/env bash
set -euo pipefail
base_commit=99b43a015d9a335cbe4765bc8ae80054391a80a5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
