#!/usr/bin/env bash
set -euo pipefail
base_commit=667dc3de34aef34fab3bbd64ed06cb419291bf4c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
