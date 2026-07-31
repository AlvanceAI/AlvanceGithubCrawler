#!/usr/bin/env bash
set -euo pipefail
base_commit=7fe5c86e7f89a17bad9fa096d4b55a28713044c7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
