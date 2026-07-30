#!/usr/bin/env bash
set -euo pipefail
base_commit=b61680d0cc2a7e47248f81499f70e9a98538a716
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
