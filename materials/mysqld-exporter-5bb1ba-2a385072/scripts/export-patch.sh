#!/usr/bin/env bash
set -euo pipefail
base_commit=2a3850727e5af11873cc715a2b1a31bedce264eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
