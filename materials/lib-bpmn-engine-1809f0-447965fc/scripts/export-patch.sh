#!/usr/bin/env bash
set -euo pipefail
base_commit=447965fc30f55be9ae6c0929a49e24d7ccf4941f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
