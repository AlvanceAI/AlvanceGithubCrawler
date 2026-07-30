#!/usr/bin/env bash
set -euo pipefail
base_commit=9a75c326df6abc7ebe44a1dcad4c24334ee8dad0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
