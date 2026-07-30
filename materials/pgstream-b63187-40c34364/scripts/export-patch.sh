#!/usr/bin/env bash
set -euo pipefail
base_commit=40c34364e740a151b7cdc3c088b12ae7445d331a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
