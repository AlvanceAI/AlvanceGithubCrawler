#!/usr/bin/env bash
set -euo pipefail
base_commit=3ceb78a4ec316c8f2be0296f58da5a89bf25eaea
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
