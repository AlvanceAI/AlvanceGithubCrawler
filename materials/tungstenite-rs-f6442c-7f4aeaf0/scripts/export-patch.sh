#!/usr/bin/env bash
set -euo pipefail
base_commit=7f4aeaf0944992c5664c8fb8e0d54577c7e18020
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
