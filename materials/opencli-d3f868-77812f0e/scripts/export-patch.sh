#!/usr/bin/env bash
set -euo pipefail
base_commit=77812f0e3dd4f2bcdd3a73b19355a1a3cf4fbd10
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
