#!/usr/bin/env bash
set -euo pipefail
base_commit=d5f7cf5b598c2eede99ad3683de0ba10f7a8736b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
