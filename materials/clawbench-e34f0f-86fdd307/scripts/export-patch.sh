#!/usr/bin/env bash
set -euo pipefail
base_commit=86fdd307b5d6f44c1ec85439fc4b7a6eea24b066
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
