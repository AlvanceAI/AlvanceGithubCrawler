#!/usr/bin/env bash
set -euo pipefail
base_commit=f2d7ff49feeaaddcdbdbad147e8b152aefcb9e5e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
