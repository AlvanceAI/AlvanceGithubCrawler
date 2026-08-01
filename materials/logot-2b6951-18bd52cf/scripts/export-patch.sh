#!/usr/bin/env bash
set -euo pipefail
base_commit=18bd52cfa01fe783c0b4ba7e8fda59b4a716058a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
