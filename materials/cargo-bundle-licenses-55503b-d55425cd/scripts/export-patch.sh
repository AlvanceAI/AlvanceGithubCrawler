#!/usr/bin/env bash
set -euo pipefail
base_commit=d55425cd47f987360f027620abe85c6503d887a1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
