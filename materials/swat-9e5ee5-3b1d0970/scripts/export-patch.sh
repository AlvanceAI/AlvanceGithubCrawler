#!/usr/bin/env bash
set -euo pipefail
base_commit=3b1d09701b7c77ed46b323551991f72ffef4ec06
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
