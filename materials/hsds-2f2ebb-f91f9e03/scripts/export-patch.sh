#!/usr/bin/env bash
set -euo pipefail
base_commit=f91f9e03b0fb12226a42baef78e57c1de629c86d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
