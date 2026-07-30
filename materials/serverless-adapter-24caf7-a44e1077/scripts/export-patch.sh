#!/usr/bin/env bash
set -euo pipefail
base_commit=a44e1077574eb5454256fccc9e783841f7afeb76
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
