#!/usr/bin/env bash
set -euo pipefail
base_commit=c6acd6a5bd041dbec42aa4e0f650dc2ea82d2857
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
