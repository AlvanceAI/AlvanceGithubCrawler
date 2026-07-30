#!/usr/bin/env bash
set -euo pipefail
base_commit=eeac3bbb791e9efa16477976806f809d46c66a7a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
