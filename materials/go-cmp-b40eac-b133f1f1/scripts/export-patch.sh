#!/usr/bin/env bash
set -euo pipefail
base_commit=b133f1f1932e48f466f597a3346ce6f5a49a0dc1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
