#!/usr/bin/env bash
set -euo pipefail
base_commit=8e357cf3a5060138dfe111b6a84df7d8f1c8ae9d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
