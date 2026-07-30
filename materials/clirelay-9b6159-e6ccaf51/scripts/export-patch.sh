#!/usr/bin/env bash
set -euo pipefail
base_commit=e6ccaf51d65323c524b25ca662c3e742606b3903
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
