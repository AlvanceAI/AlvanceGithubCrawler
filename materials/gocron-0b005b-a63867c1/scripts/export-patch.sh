#!/usr/bin/env bash
set -euo pipefail
base_commit=a63867c19b5616fb495c08c2437b5ad1da9f547f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
