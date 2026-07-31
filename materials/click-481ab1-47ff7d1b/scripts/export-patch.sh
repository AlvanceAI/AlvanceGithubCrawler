#!/usr/bin/env bash
set -euo pipefail
base_commit=47ff7d1b93432e285f86f3c77cfa0e610a65b0a5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
