#!/usr/bin/env bash
set -euo pipefail
base_commit=9619c06d06e738a3fd632ae98724c7cbe9245f1d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
