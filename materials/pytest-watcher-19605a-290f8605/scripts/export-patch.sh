#!/usr/bin/env bash
set -euo pipefail
base_commit=290f860579f7fbc641f406ed8b09795dc1a77a02
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
