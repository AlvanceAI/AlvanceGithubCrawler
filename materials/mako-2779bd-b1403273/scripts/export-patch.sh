#!/usr/bin/env bash
set -euo pipefail
base_commit=b14032734c9acb6f84ab684b73b9708554c04e8b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
