#!/usr/bin/env bash
set -euo pipefail
base_commit=aac184e9340fe39098328055a6211805c3198aea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
