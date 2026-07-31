#!/usr/bin/env bash
set -euo pipefail
base_commit=7809486a9716faa2234c8a45d88b601034de52d8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
