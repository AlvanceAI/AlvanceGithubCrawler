#!/usr/bin/env bash
set -euo pipefail
base_commit=579a4be6cbce5bd613cdb647b685c2b7b271b266
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
