#!/usr/bin/env bash
set -euo pipefail
base_commit=9025287d6bc8123d87832097d8e46bfbd5a24881
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
