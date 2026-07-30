#!/usr/bin/env bash
set -euo pipefail
base_commit=4e515e5036af32a5df713d1be8050978a5613fb7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
