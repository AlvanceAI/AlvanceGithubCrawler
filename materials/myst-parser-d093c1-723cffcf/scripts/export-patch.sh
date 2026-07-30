#!/usr/bin/env bash
set -euo pipefail
base_commit=723cffcf84213f0cb58695b27eec9ad72052b53a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
