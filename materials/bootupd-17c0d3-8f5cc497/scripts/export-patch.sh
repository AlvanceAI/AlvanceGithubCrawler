#!/usr/bin/env bash
set -euo pipefail
base_commit=8f5cc4972f31fc00c6b19e3b3547cb2cf18795fd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
