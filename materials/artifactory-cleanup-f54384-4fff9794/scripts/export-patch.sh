#!/usr/bin/env bash
set -euo pipefail
base_commit=4fff9794d6d35d09c19d63bd4c1f477361f97483
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
