#!/usr/bin/env bash
set -euo pipefail
base_commit=8836f5c0e8eacdc5233911754b94e70917cf0dba
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
