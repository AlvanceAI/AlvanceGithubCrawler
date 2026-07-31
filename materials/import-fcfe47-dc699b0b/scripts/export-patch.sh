#!/usr/bin/env bash
set -euo pipefail
base_commit=dc699b0bb1e465e570c6127137b3f116337accf6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
