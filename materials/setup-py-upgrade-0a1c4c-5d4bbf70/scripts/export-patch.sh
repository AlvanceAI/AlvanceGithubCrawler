#!/usr/bin/env bash
set -euo pipefail
base_commit=5d4bbf70ca79aefe2386ef637f6c61e0b9fb1003
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
