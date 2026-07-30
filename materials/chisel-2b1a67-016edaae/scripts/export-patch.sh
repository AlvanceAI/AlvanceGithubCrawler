#!/usr/bin/env bash
set -euo pipefail
base_commit=016edaae00d6761bfe67ce184c5f27e6965a301d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
