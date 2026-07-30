#!/usr/bin/env bash
set -euo pipefail
base_commit=9466647a1845f1f5c8b8b73b28ea45ff0e6d73e3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
