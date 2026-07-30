#!/usr/bin/env bash
set -euo pipefail
base_commit=b7401a051c0ce1b1ec3f2713590a78585adf9ae1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
