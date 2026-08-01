#!/usr/bin/env bash
set -euo pipefail
base_commit=01ad037ec66cee85bd3efb766091e073c9c53035
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
