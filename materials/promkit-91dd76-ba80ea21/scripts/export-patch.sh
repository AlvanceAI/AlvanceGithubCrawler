#!/usr/bin/env bash
set -euo pipefail
base_commit=ba80ea211085d7984033b7f454364863f7c7c884
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
