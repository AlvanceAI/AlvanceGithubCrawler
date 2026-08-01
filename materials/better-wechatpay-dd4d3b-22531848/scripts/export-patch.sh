#!/usr/bin/env bash
set -euo pipefail
base_commit=2253184804467d7078a30da89bed965bc78c7187
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
