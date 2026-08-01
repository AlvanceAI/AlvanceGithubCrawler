#!/usr/bin/env bash
set -euo pipefail
base_commit=490b3a7c39e9e08f75363e256cea30f96b39a409
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
