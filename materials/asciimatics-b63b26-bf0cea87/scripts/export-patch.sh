#!/usr/bin/env bash
set -euo pipefail
base_commit=bf0cea87b50439e40a5c7b708d64da4195314a60
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
