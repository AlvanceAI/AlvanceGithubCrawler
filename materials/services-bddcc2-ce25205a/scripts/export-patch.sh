#!/usr/bin/env bash
set -euo pipefail
base_commit=ce25205adf873830449078ff54f705edc64778e9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
