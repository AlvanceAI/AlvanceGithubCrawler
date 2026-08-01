#!/usr/bin/env bash
set -euo pipefail
base_commit=459c7137158b6fc803bf631061d9fc714a2df4c9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
