#!/usr/bin/env bash
set -euo pipefail
base_commit=4f66f32e160f16d73dee5eed52cd91984935763f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
