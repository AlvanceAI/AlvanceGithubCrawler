#!/usr/bin/env bash
set -euo pipefail
base_commit=f3522c0b51477ceb104e0285efa1f8dc0d2cfad0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
