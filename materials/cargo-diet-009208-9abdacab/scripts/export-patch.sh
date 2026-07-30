#!/usr/bin/env bash
set -euo pipefail
base_commit=9abdacab2b9b649e7505326677852a4943fc9c30
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
