#!/usr/bin/env bash
set -euo pipefail
base_commit=7b2c0df0cfcf5b4891404f9b99bce3966b68101a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
