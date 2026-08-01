#!/usr/bin/env bash
set -euo pipefail
base_commit=4dd80223e35446baa6c963d66e7b0678c897dbb4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
