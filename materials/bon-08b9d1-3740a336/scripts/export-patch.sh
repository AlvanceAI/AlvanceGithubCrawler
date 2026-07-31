#!/usr/bin/env bash
set -euo pipefail
base_commit=3740a336ae9b7487226378049fcac0dc50ff1446
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
