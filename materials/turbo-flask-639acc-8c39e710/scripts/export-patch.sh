#!/usr/bin/env bash
set -euo pipefail
base_commit=8c39e71079a85f11bfaa38ff6f04617decef4e37
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
