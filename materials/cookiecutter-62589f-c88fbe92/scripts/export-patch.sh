#!/usr/bin/env bash
set -euo pipefail
base_commit=c88fbe921c97c58b65f1883ba90a0ab53cc91b34
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
