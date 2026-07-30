#!/usr/bin/env bash
set -euo pipefail
base_commit=3772c2fe7b79343db4ae20e1adf14f2342f96cd1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
