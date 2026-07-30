#!/usr/bin/env bash
set -euo pipefail
base_commit=d441d94d999daf4a1b5727e462ba36691962007e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
