#!/usr/bin/env bash
set -euo pipefail
base_commit=003f1faecd54e3fa7ee8502d3ca31431a95766e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
