#!/usr/bin/env bash
set -euo pipefail
base_commit=9fde1364c4ff98663d486d2e84504bfb8a71f54e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
