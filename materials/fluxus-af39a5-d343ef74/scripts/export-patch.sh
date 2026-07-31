#!/usr/bin/env bash
set -euo pipefail
base_commit=d343ef7432e1a47d0f51e14b030766b5c5ae528f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
