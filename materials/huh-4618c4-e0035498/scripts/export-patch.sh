#!/usr/bin/env bash
set -euo pipefail
base_commit=e0035498085e722ddeee4c59c8e540f4c20f7661
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
