#!/usr/bin/env bash
set -euo pipefail
base_commit=1ef4b4685b27bd5c105d9459dfad874f0e43c06d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
