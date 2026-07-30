#!/usr/bin/env bash
set -euo pipefail
base_commit=197fa4accdf542111c52b8ebf184e463cf84aa72
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
