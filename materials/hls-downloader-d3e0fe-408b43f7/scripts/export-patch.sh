#!/usr/bin/env bash
set -euo pipefail
base_commit=408b43f7c0f73ea7efd4153199f3935e38e657eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
