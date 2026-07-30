#!/usr/bin/env bash
set -euo pipefail
base_commit=3ae8aad218fa56e57c57f4050f3c8b6b01266932
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
