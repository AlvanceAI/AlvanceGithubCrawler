#!/usr/bin/env bash
set -euo pipefail
base_commit=f121db94017a100c0f792b3810e2591d49db9c39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
