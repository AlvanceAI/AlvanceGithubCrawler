#!/usr/bin/env bash
set -euo pipefail
base_commit=2864494b200f5640de381d91e578db64a3d2a409
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
