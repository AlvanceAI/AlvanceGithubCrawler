#!/usr/bin/env bash
set -euo pipefail
base_commit=d805f30275e279907cbad8a339a3d899fc0ea8d8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
