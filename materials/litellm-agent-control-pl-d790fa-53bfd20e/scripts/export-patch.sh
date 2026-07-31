#!/usr/bin/env bash
set -euo pipefail
base_commit=53bfd20e2fec51fc8f665fb614512c6b138367da
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
