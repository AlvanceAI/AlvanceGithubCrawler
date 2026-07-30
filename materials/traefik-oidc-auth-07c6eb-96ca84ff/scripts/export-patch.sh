#!/usr/bin/env bash
set -euo pipefail
base_commit=96ca84ffe50587070b4036ba8b15cde9ed8aadc2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
