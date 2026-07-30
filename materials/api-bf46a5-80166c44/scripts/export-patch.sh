#!/usr/bin/env bash
set -euo pipefail
base_commit=80166c444cbf7d60d0b9f4616fb4023ba2908f17
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
