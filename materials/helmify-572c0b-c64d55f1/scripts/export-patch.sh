#!/usr/bin/env bash
set -euo pipefail
base_commit=c64d55f12c22f9305898916c9d71e3b443fa45f2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
