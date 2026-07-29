#!/usr/bin/env bash
set -euo pipefail
base_commit=0a944f09a9b6cf96e8c92e8a3ceb915dbebfd46f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
