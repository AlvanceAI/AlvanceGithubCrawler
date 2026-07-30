#!/usr/bin/env bash
set -euo pipefail
base_commit=cd2ef47d5f1c834680ae4b6fa3ad57daa58edffc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
