#!/usr/bin/env bash
set -euo pipefail
base_commit=c82f96841a9edc156221a2365661a00f340b764e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
