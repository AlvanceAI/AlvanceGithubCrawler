#!/usr/bin/env bash
set -euo pipefail
base_commit=e309d1a679af9684f4540952686fb0ba9971126d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
