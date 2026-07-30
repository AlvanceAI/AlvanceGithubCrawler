#!/usr/bin/env bash
set -euo pipefail
base_commit=e1952d30108d57f4528f88c4a0b890494d99b6b7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
