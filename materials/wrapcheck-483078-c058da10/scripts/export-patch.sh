#!/usr/bin/env bash
set -euo pipefail
base_commit=c058da1005e26566820d7eb858899c280d87eab9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
