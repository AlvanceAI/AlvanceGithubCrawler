#!/usr/bin/env bash
set -euo pipefail
base_commit=e800285910913db9a3afc2bc53a846fa64b0c747
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
