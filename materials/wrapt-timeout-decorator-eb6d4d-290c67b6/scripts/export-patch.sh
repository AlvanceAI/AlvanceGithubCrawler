#!/usr/bin/env bash
set -euo pipefail
base_commit=290c67b64b14bf376d0d122cf4d2ccbe038c1b51
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
