#!/usr/bin/env bash
set -euo pipefail
base_commit=f23c2955be810801f2d6c51c4185b1fb389cb0e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
