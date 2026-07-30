#!/usr/bin/env bash
set -euo pipefail
base_commit=083d18025137bc3e6359cad61bafb9929563ab75
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
