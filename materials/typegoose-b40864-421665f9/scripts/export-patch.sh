#!/usr/bin/env bash
set -euo pipefail
base_commit=421665f91c7bd6ef2472076ac14ab3976c4b0731
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
