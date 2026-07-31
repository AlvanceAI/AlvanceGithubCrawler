#!/usr/bin/env bash
set -euo pipefail
base_commit=3a76cfee02a00ee6ce20eeac6447573b34f25d86
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
