#!/usr/bin/env bash
set -euo pipefail
base_commit=5696b2800bc692e6cc372ee8232da6d3f7e7387f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
