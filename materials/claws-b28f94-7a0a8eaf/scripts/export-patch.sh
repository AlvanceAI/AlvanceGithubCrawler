#!/usr/bin/env bash
set -euo pipefail
base_commit=7a0a8eaf1f3538bd63407176b3e4be96012944d4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
