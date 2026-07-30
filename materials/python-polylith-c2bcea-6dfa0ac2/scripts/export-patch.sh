#!/usr/bin/env bash
set -euo pipefail
base_commit=6dfa0ac2386342bae4086f08aabd86655aa1f191
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
