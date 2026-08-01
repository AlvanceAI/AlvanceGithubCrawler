#!/usr/bin/env bash
set -euo pipefail
base_commit=073b7858d8906b2ce88c2b65d969b9593557808b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
