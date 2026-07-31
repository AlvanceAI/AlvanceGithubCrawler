#!/usr/bin/env bash
set -euo pipefail
base_commit=b56329354ce0ecbe4afe7c85f7b76417678a5ef8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
