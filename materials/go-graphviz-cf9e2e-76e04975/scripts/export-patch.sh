#!/usr/bin/env bash
set -euo pipefail
base_commit=76e04975df88d41930377420c9a3170ef0031379
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
