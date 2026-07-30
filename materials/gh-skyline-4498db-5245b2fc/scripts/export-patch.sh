#!/usr/bin/env bash
set -euo pipefail
base_commit=5245b2fc95250075cac37d24a4cd9b09258de5a8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
