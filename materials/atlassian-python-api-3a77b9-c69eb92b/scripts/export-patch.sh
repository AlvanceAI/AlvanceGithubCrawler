#!/usr/bin/env bash
set -euo pipefail
base_commit=c69eb92ba214c2f21e93f1e25a24fe314cd75e11
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
