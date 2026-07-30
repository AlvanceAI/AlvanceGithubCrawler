#!/usr/bin/env bash
set -euo pipefail
base_commit=a80f2799d7b9ed676f814a308464c1837d23bbcf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
