#!/usr/bin/env bash
set -euo pipefail
base_commit=5ae90bfcbd7ab2f69809b094601f7975c32ae077
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
