#!/usr/bin/env bash
set -euo pipefail
base_commit=315a75ab1025fce0b85de881cac39214a455fd90
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
