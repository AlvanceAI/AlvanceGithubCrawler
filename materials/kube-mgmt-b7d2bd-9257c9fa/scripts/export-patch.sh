#!/usr/bin/env bash
set -euo pipefail
base_commit=9257c9fabb6fbe005e65c3f2b6d2b626399b18e7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
