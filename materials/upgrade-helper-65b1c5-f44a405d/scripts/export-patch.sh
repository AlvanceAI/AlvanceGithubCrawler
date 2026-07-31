#!/usr/bin/env bash
set -euo pipefail
base_commit=f44a405d9834c797d527c87dbf05d5b7d636367b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
