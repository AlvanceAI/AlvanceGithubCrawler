#!/usr/bin/env bash
set -euo pipefail
base_commit=04dc1947315f322825991b5dc637604567703c9c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
