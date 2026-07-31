#!/usr/bin/env bash
set -euo pipefail
base_commit=7c4b2f4ddb560835c227aa75edd7dc3b57740d37
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
