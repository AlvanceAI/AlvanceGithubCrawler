#!/usr/bin/env bash
set -euo pipefail
base_commit=f1e7554014296f3d97b2367c524a14b3b8877ab6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
