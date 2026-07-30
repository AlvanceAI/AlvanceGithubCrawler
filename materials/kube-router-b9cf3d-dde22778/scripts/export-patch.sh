#!/usr/bin/env bash
set -euo pipefail
base_commit=dde2277822934ddeaa37cdc39b8707830d6781d2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
