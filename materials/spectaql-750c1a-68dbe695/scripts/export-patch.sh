#!/usr/bin/env bash
set -euo pipefail
base_commit=68dbe695f816526c5f5909260b9bd557af7f78dc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
