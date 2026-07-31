#!/usr/bin/env bash
set -euo pipefail
base_commit=e8fbb2561481ef6e711a770f0234e9379dc76892
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
