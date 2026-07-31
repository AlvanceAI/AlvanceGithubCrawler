#!/usr/bin/env bash
set -euo pipefail
base_commit=d7fbaf3a326634443e1372f216e3969657a288ba
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
