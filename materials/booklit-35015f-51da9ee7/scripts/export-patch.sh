#!/usr/bin/env bash
set -euo pipefail
base_commit=51da9ee7c2688a93a07d11fb2bb3a52d3dc764cf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
