#!/usr/bin/env bash
set -euo pipefail
base_commit=1e995e0fd42091e54fc22edbb6dae1a58d4bc85e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
