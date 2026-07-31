#!/usr/bin/env bash
set -euo pipefail
base_commit=78577dc52fb738d17e9c6c49d010142a68bb186a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
