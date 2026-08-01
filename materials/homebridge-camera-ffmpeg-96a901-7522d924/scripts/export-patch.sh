#!/usr/bin/env bash
set -euo pipefail
base_commit=7522d924bedf922b3a7a4d71d35eb722dd3d790e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
