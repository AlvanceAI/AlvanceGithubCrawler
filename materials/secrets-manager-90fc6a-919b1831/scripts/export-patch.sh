#!/usr/bin/env bash
set -euo pipefail
base_commit=919b1831159f25ca60bd4b6faf20a17e75a5bdd7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
