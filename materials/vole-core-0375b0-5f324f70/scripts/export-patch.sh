#!/usr/bin/env bash
set -euo pipefail
base_commit=5f324f704b821e322297d204fc17f8b8ea1c9029
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
