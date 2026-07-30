#!/usr/bin/env bash
set -euo pipefail
base_commit=e940b1dca6f4e1ca05e443c105fe25e9512bfc08
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
