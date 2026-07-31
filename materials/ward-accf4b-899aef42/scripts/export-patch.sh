#!/usr/bin/env bash
set -euo pipefail
base_commit=899aef42e779d8385668d92f319d8523f0b72e0d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
