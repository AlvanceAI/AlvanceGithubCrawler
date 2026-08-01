#!/usr/bin/env bash
set -euo pipefail
base_commit=41296284ac269b997f91c996a5345b6d0db67530
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
