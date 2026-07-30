#!/usr/bin/env bash
set -euo pipefail
base_commit=8b8e010ab4a7a16a66cac6bea48f861551a18739
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
