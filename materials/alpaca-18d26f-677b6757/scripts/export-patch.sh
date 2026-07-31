#!/usr/bin/env bash
set -euo pipefail
base_commit=677b6757487fd6af0e7e4ccb61c4f649e10a1096
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
