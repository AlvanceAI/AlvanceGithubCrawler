#!/usr/bin/env bash
set -euo pipefail
base_commit=71018835a6ccd28558513614af9e7d77ee921fe4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
