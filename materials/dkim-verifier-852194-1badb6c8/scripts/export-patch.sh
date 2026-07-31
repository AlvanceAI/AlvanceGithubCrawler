#!/usr/bin/env bash
set -euo pipefail
base_commit=1badb6c8d639bd5973f870fa7bfc6f96facba9ca
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
