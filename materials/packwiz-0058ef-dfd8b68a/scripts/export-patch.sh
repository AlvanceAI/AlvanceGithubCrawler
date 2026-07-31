#!/usr/bin/env bash
set -euo pipefail
base_commit=dfd8b68a4796c763e25bad50265ea1f1233e24f1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
