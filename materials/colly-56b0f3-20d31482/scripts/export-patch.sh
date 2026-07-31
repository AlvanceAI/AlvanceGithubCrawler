#!/usr/bin/env bash
set -euo pipefail
base_commit=20d31482af5f754832a753f88517f3dfa61d921f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
