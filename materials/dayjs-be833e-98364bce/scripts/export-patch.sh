#!/usr/bin/env bash
set -euo pipefail
base_commit=98364bcebc047529345cc8c2bbcc44a6a8c18e79
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
