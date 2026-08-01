#!/usr/bin/env bash
set -euo pipefail
base_commit=f47b4464e8064d873250a78c68beac17bc2941fd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
