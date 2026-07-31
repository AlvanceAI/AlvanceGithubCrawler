#!/usr/bin/env bash
set -euo pipefail
base_commit=22e833c29a7039abb0eba39c642189234df92bc0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
