#!/usr/bin/env bash
set -euo pipefail
base_commit=a77e402c73a57012b148cbf6453d0a176871ef23
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
