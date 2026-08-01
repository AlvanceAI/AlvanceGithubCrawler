#!/usr/bin/env bash
set -euo pipefail
base_commit=a49d61bb50c7cf898e1687023666416ab1d5ae39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
