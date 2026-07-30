#!/usr/bin/env bash
set -euo pipefail
base_commit=3affec856c2216ae1c4856d849367ea557c5dc93
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
