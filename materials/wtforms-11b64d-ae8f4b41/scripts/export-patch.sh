#!/usr/bin/env bash
set -euo pipefail
base_commit=ae8f4b41332a5a0fe6e8a14839487c476c175ba7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
