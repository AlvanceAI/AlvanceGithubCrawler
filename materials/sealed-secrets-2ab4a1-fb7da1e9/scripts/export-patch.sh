#!/usr/bin/env bash
set -euo pipefail
base_commit=fb7da1e9ba98dfda0e068d6a3849ab2a40adc9d0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
