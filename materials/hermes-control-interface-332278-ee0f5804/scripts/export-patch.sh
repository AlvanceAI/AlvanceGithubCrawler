#!/usr/bin/env bash
set -euo pipefail
base_commit=ee0f5804e631ce522cb709fccae38fc68d3681e1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
