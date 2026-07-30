#!/usr/bin/env bash
set -euo pipefail
base_commit=fb944fe955ab451f0a339636ea140eebd1a83608
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
