#!/usr/bin/env bash
set -euo pipefail
base_commit=bda6eca2979ae19ac0917f914093721c88813726
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
