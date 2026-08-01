#!/usr/bin/env bash
set -euo pipefail
base_commit=23194e40dba29d03ba0b9aef8a08955b8cf16d12
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
