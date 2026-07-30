#!/usr/bin/env bash
set -euo pipefail
base_commit=585d48134e7b71be74d8b81b54cdbd07f6f1a1c4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
