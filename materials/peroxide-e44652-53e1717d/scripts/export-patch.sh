#!/usr/bin/env bash
set -euo pipefail
base_commit=53e1717d8eba948791d03802a5494cd94c5e5e76
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
