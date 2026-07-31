#!/usr/bin/env bash
set -euo pipefail
base_commit=64a01ebbc71b450ba88f8e41b759aeadd4fcf4fd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
