#!/usr/bin/env bash
set -euo pipefail
base_commit=a6f3c064d733dc79b9498b5a951d2d73146576ab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
