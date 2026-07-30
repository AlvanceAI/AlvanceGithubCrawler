#!/usr/bin/env bash
set -euo pipefail
base_commit=006ac8976f52af356beb5042788370f645f6da02
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
