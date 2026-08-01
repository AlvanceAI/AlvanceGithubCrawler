#!/usr/bin/env bash
set -euo pipefail
base_commit=d237f4c00f1ac2cae9ea2b3d5dd93dd64d465073
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
