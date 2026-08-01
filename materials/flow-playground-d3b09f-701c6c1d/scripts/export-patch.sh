#!/usr/bin/env bash
set -euo pipefail
base_commit=701c6c1daefbac163ea54f05c8116a3777239642
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
