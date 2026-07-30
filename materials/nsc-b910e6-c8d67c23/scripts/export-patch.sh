#!/usr/bin/env bash
set -euo pipefail
base_commit=c8d67c23c187ed0db496ce5b2b66e96715bb72bf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
