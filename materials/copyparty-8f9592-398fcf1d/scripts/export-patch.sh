#!/usr/bin/env bash
set -euo pipefail
base_commit=398fcf1d18d28a75a9f234765c15b777fbb6bdea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
