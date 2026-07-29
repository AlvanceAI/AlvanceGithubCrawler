#!/usr/bin/env bash
set -euo pipefail
base_commit=d7368c858851719e53551bc96b85e4fafea94669
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
