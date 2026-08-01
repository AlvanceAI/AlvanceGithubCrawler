#!/usr/bin/env bash
set -euo pipefail
base_commit=ae5c3fede5ca489fd7eaa8271e9d9c5eabc88e98
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
