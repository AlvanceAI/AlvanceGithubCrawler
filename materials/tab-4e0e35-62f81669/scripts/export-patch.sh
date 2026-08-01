#!/usr/bin/env bash
set -euo pipefail
base_commit=62f816696f4faec73fd3fc98d57dac10061ba025
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
