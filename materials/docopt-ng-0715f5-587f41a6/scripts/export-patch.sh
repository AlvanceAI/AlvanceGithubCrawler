#!/usr/bin/env bash
set -euo pipefail
base_commit=587f41a61437b680b4215de1874fb6975d8a49d6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
