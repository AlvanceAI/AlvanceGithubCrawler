#!/usr/bin/env bash
set -euo pipefail
base_commit=791a8e3018417c0c62d116001cd44a811fed86ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
