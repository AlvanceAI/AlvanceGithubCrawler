#!/usr/bin/env bash
set -euo pipefail
base_commit=499f01298ecddd7ddfff7b289bab8b45b4f763e3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
