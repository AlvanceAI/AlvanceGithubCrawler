#!/usr/bin/env bash
set -euo pipefail
base_commit=8916430616f56ce26649cd0aae285e72d9eedf0d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
