#!/usr/bin/env bash
set -euo pipefail
base_commit=635569603f9c1e59b3505d9f5b818da77f46805c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
