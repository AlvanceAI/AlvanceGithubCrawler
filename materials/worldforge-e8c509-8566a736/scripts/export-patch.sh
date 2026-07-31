#!/usr/bin/env bash
set -euo pipefail
base_commit=8566a736c07c7454d11f2dc3a8dfabf2ab86d0da
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
