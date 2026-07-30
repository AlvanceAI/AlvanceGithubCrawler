#!/usr/bin/env bash
set -euo pipefail
base_commit=4652011b74f330c7fde73ecd1f8d31eb7743f4d8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
