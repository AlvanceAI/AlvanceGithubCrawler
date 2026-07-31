#!/usr/bin/env bash
set -euo pipefail
base_commit=65c88cc2b3e6bdf24c8be912c6a503a6d68d0fa0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
