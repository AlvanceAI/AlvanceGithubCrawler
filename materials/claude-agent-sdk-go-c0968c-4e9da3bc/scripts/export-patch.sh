#!/usr/bin/env bash
set -euo pipefail
base_commit=4e9da3bcc976941b5b34765d2536239651540b5a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
