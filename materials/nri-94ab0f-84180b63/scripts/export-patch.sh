#!/usr/bin/env bash
set -euo pipefail
base_commit=84180b63351d03b54a317a265ba01e3e9db19f24
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
