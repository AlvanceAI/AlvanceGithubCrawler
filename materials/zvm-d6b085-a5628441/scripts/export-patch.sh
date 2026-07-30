#!/usr/bin/env bash
set -euo pipefail
base_commit=a5628441289b2a15656f137d9c228a79ef11dcc9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
