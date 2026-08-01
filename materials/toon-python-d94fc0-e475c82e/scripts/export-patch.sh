#!/usr/bin/env bash
set -euo pipefail
base_commit=e475c82e9da03dfaf88c0b277dee6b5d17100b13
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
