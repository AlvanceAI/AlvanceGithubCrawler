#!/usr/bin/env bash
set -euo pipefail
base_commit=8fc823481d58c76b804e0ccf2d55c9777b76f65d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
