#!/usr/bin/env bash
set -euo pipefail
base_commit=f63f54a73591f7a7befc1a72fc30e9b8070154ed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
