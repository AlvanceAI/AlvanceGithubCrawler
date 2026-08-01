#!/usr/bin/env bash
set -euo pipefail
base_commit=bcadbdfce78d10eb69ed9fd7cb821c965c7083b7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
