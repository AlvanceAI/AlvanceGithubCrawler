#!/usr/bin/env bash
set -euo pipefail
base_commit=77b31b715f22150817def8b2f69451e31327a2d5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
