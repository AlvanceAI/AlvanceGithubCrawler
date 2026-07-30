#!/usr/bin/env bash
set -euo pipefail
base_commit=1c248a36c3a226ef5bffd400f612d8958d197cb1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
