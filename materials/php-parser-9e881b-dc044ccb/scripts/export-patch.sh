#!/usr/bin/env bash
set -euo pipefail
base_commit=dc044ccbe9ac00e2a88f23eee3093ae24937824a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
