#!/usr/bin/env bash
set -euo pipefail
base_commit=e8713c00f6fa0e10bc3cc6a34bd10a46c5b650c2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
