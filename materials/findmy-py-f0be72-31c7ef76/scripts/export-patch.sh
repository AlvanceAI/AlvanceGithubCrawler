#!/usr/bin/env bash
set -euo pipefail
base_commit=31c7ef762b62c4cfb92d38aa576a127f0adee997
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
