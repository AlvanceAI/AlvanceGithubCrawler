#!/usr/bin/env bash
set -euo pipefail
base_commit=632d2e764de4fa5dd37ddea5d1d6c61a0324784e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
