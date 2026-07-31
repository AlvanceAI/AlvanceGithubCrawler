#!/usr/bin/env bash
set -euo pipefail
base_commit=e545b0012feb930e98fec0c441fd85958b84b1c3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
