#!/usr/bin/env bash
set -euo pipefail
base_commit=9f954cd29f2cc8f96de5ab9dcc0dd77c4446b623
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
