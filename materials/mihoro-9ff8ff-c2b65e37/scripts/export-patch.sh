#!/usr/bin/env bash
set -euo pipefail
base_commit=c2b65e374d9d8a27f4eb3d2d2b5136d028563438
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
