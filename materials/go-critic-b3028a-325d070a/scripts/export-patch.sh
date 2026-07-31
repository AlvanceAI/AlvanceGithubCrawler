#!/usr/bin/env bash
set -euo pipefail
base_commit=325d070a6839c2f5958f2d587d466730d7ea2e3a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
