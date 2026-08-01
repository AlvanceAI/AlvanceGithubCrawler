#!/usr/bin/env bash
set -euo pipefail
base_commit=89b843b346c6baf2b209dacfe1c9a83f244ee222
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
