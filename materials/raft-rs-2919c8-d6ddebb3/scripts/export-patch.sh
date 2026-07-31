#!/usr/bin/env bash
set -euo pipefail
base_commit=d6ddebb30a790ca7975c81aa76eef2851ca39d3e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
