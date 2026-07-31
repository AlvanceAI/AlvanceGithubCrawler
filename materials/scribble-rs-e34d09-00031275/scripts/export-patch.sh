#!/usr/bin/env bash
set -euo pipefail
base_commit=000312758ce98ca6280880ea5ab57d28d1215a2e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
