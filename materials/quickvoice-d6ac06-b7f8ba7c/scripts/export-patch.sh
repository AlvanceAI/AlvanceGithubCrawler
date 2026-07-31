#!/usr/bin/env bash
set -euo pipefail
base_commit=b7f8ba7c4e9df178a716240c732cd9c6cfb41771
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
