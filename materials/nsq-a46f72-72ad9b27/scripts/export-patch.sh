#!/usr/bin/env bash
set -euo pipefail
base_commit=72ad9b2793578ee909ee8d57fc6fcbf7ec2e7144
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
