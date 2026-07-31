#!/usr/bin/env bash
set -euo pipefail
base_commit=cd8d8f8e7b383d85a28cd7477c71494bab8889e7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
