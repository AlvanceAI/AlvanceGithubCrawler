#!/usr/bin/env bash
set -euo pipefail
base_commit=a3d8fe146ad4166c8b3e8fbb90f944216ca25e8a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
