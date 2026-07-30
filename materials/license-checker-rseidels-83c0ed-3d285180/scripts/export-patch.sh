#!/usr/bin/env bash
set -euo pipefail
base_commit=3d28518039b2171009109f0a5fc810d29db774fd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
