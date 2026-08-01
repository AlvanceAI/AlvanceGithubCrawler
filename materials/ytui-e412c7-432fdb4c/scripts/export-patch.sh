#!/usr/bin/env bash
set -euo pipefail
base_commit=432fdb4cbe9a982c18954c5c7c72f12fcc01eae6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
