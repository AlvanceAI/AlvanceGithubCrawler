#!/usr/bin/env bash
set -euo pipefail
base_commit=8657322d35988632a0d57b402e61fd5a8fe9b4e0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
