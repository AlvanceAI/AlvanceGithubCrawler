#!/usr/bin/env bash
set -euo pipefail
base_commit=45e962b4439e6476d67937206566c0470743c660
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
