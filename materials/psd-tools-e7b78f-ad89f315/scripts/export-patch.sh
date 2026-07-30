#!/usr/bin/env bash
set -euo pipefail
base_commit=ad89f315777866c832bf82e0377226cb13250c36
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
