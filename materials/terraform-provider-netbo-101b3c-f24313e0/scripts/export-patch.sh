#!/usr/bin/env bash
set -euo pipefail
base_commit=f24313e0d8fd47a1b3aa09e7a061e46cb731434e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
