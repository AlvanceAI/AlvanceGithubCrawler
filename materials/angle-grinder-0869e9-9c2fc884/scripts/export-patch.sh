#!/usr/bin/env bash
set -euo pipefail
base_commit=9c2fc8846d7e950160579ef0b2d7ca56a76688e9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
