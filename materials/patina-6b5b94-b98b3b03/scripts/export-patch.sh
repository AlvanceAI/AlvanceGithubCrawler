#!/usr/bin/env bash
set -euo pipefail
base_commit=b98b3b03e885e6996750d88f7b851010be6ed912
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
