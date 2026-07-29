#!/usr/bin/env bash
set -euo pipefail
base_commit=2924772fb4439b8aca40b1bffca70088acba5a1b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
