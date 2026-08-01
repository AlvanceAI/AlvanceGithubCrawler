#!/usr/bin/env bash
set -euo pipefail
base_commit=1da71a7dc254851043dc0060b362a1b6d72f01e7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
