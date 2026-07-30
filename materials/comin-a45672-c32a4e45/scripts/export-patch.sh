#!/usr/bin/env bash
set -euo pipefail
base_commit=c32a4e457cd3bc99d6c18631707e9d8294f4b5d0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
