#!/usr/bin/env bash
set -euo pipefail
base_commit=c779e8fd1eaeee44f31ecb186f9d798783cd3ba4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
