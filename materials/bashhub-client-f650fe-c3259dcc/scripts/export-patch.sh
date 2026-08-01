#!/usr/bin/env bash
set -euo pipefail
base_commit=c3259dcc0f6b4bb9f347e4ee980023864fa2bfc9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
