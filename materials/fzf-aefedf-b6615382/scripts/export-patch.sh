#!/usr/bin/env bash
set -euo pipefail
base_commit=b66153825fa5186ade46a743e1418253482262bd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
