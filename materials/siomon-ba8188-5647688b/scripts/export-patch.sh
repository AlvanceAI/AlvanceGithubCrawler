#!/usr/bin/env bash
set -euo pipefail
base_commit=5647688bdfe011d761b972d8387fa285cd9a4be2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
