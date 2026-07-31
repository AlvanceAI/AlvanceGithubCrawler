#!/usr/bin/env bash
set -euo pipefail
base_commit=ad13f3d90780f53aea2488c6a4b76c0d334bf136
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
