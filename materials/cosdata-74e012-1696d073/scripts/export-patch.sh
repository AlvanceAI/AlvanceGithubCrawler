#!/usr/bin/env bash
set -euo pipefail
base_commit=1696d0737aeb0ba4f786d42705d3623d9aa4868d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
