#!/usr/bin/env bash
set -euo pipefail
base_commit=4d22f69b909411ceb5ccfa769feba4d8428b5ded
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
