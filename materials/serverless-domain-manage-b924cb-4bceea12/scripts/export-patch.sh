#!/usr/bin/env bash
set -euo pipefail
base_commit=4bceea12be67d0072ecdbac850484b9acba77574
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
