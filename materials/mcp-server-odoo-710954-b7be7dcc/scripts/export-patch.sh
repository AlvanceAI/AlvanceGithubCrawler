#!/usr/bin/env bash
set -euo pipefail
base_commit=b7be7dcc0c422275da2d61a8e422ef5414156abd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
