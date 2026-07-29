#!/usr/bin/env bash
set -euo pipefail
base_commit=ba294586bd91bba94a9085d83a599e486b9d0656
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
