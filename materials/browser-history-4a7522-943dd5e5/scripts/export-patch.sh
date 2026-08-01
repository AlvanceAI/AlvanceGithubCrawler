#!/usr/bin/env bash
set -euo pipefail
base_commit=943dd5e5d14246b8fbdb05874b56544cfb220e07
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
