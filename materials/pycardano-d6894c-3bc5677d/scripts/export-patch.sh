#!/usr/bin/env bash
set -euo pipefail
base_commit=3bc5677d4db6c5e49de11bffd302a7ffe4e6bcff
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
