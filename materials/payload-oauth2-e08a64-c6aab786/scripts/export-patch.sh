#!/usr/bin/env bash
set -euo pipefail
base_commit=c6aab78667cad66451f7f3c877a4d723d841033a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
