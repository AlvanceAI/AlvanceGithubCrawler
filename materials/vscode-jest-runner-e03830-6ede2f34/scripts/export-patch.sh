#!/usr/bin/env bash
set -euo pipefail
base_commit=6ede2f34a9e838af53362bfad1a027f580a3f748
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
