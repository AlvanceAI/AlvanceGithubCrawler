#!/usr/bin/env bash
set -euo pipefail
base_commit=f063ba01bd9e698d16bf0bf8101af87c0e0f16d4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
