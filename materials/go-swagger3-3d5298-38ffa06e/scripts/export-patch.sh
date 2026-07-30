#!/usr/bin/env bash
set -euo pipefail
base_commit=38ffa06e310898ae46f5ac171e06ba5d33d39c20
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
