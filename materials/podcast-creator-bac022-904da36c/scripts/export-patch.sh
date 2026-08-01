#!/usr/bin/env bash
set -euo pipefail
base_commit=904da36cca12846e8c610fff5cab2972735b007d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
