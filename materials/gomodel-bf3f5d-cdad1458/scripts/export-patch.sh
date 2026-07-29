#!/usr/bin/env bash
set -euo pipefail
base_commit=cdad1458fcab07936583e10042c841c7e301bd62
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
