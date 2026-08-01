#!/usr/bin/env bash
set -euo pipefail
base_commit=cddbfa1fad7c664b9aa2612ccb18b85595fa840d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
