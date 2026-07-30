#!/usr/bin/env bash
set -euo pipefail
base_commit=eaeba4e98b388b8d1d31a31572d91ff989e04c00
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
