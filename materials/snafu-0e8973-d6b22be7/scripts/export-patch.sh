#!/usr/bin/env bash
set -euo pipefail
base_commit=d6b22be7e31fdd308bfe637349263781edcaac29
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
