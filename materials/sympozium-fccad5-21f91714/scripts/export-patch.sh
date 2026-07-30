#!/usr/bin/env bash
set -euo pipefail
base_commit=21f91714820e767c64406d39a3b1219f5a2969eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
