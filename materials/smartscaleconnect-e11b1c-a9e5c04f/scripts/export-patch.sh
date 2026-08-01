#!/usr/bin/env bash
set -euo pipefail
base_commit=a9e5c04f1079b65d456c8a5fd296775a1ef29e8f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
