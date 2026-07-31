#!/usr/bin/env bash
set -euo pipefail
base_commit=14e3e4914ad5128c68f6bbf4ab40ae1de19b342e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
