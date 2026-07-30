#!/usr/bin/env bash
set -euo pipefail
base_commit=c07436dd14fae60a33ce23974e30aa1ef5ed4f96
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
