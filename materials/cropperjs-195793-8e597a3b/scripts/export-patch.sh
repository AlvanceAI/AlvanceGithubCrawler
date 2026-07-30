#!/usr/bin/env bash
set -euo pipefail
base_commit=8e597a3b11e514bafc1e558f30f398ed574fcded
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
