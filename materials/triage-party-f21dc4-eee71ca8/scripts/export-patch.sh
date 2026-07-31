#!/usr/bin/env bash
set -euo pipefail
base_commit=eee71ca8dedfd45495cfc5d5f65834df6415f4df
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
