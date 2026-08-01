#!/usr/bin/env bash
set -euo pipefail
base_commit=a95f4d421ffa602723cb5ac2606bd854e1dfc49a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
