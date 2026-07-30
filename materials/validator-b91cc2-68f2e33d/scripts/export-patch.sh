#!/usr/bin/env bash
set -euo pipefail
base_commit=68f2e33d236f579ae7bf42c82cf2ca7986f176f6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
