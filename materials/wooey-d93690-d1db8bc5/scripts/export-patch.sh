#!/usr/bin/env bash
set -euo pipefail
base_commit=d1db8bc506d266cf687897b9585c2614605468d6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
