#!/usr/bin/env bash
set -euo pipefail
base_commit=a52885cd7090af18e54dcd586ce268efb64605ab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
