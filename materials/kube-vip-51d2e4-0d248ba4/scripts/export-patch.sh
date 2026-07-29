#!/usr/bin/env bash
set -euo pipefail
base_commit=0d248ba40fd7004050f258b615ed6cfceac932b6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
