#!/usr/bin/env bash
set -euo pipefail
base_commit=da66dd73899222b6c71dfe59ffeba5040e1b73c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
