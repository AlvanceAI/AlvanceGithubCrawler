#!/usr/bin/env bash
set -euo pipefail
base_commit=d6e2282579189af2fc104ab541faec3076869718
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
