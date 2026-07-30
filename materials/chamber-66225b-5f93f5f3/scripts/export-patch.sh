#!/usr/bin/env bash
set -euo pipefail
base_commit=5f93f5f357740686db56a037935b4dfd9805ca57
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
