#!/usr/bin/env bash
set -euo pipefail
base_commit=8ed1ebe19822c944f0a85dc848ca4908184f6c48
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
