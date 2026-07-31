#!/usr/bin/env bash
set -euo pipefail
base_commit=ed8d6d0c3722c9e7e40d361c5688ab1bd9e4ffa1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
