#!/usr/bin/env bash
set -euo pipefail
base_commit=8f10a7c67b6b1eba1dccb66621dc39221f1562a4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
