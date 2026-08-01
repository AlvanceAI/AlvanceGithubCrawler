#!/usr/bin/env bash
set -euo pipefail
base_commit=32e3ab3243415b7bf46f812d933f4d29862e3046
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
