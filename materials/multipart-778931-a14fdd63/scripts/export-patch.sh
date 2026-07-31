#!/usr/bin/env bash
set -euo pipefail
base_commit=a14fdd637f1a69b6e8db06603489ac495efd1bb2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
