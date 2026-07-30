#!/usr/bin/env bash
set -euo pipefail
base_commit=a9426ee256b61ce9a10ad735b620048efd156ea1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
