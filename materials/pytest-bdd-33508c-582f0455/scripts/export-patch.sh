#!/usr/bin/env bash
set -euo pipefail
base_commit=582f045534618756da979433e6db30ce68894002
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
