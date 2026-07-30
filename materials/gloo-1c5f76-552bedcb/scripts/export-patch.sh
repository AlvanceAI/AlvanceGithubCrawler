#!/usr/bin/env bash
set -euo pipefail
base_commit=552bedcb2ca8c384edc8f66d6bdda6a5e7ec3697
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
