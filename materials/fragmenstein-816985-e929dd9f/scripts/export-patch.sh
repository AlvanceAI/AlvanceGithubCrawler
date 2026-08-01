#!/usr/bin/env bash
set -euo pipefail
base_commit=e929dd9fed1b41224b6ce8521a9362d106c4915f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
