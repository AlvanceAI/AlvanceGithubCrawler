#!/usr/bin/env bash
set -euo pipefail
base_commit=98677e68325b07b89634fb6236ad776535267982
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
