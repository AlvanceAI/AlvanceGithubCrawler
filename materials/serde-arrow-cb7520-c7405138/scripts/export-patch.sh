#!/usr/bin/env bash
set -euo pipefail
base_commit=c74051388b6ff58277545997c557b0d896c479e1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
