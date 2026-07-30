#!/usr/bin/env bash
set -euo pipefail
base_commit=0155eaf70114f5ed3cbb172968eceaf6106940f7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
