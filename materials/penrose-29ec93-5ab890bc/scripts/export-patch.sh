#!/usr/bin/env bash
set -euo pipefail
base_commit=5ab890bc98a06c450bfec40c405829c3cf68982c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
