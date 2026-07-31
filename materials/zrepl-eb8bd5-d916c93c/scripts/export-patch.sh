#!/usr/bin/env bash
set -euo pipefail
base_commit=d916c93cf939711d6632b0c8e812c04ffcaaf5ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
