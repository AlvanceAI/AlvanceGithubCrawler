#!/usr/bin/env bash
set -euo pipefail
base_commit=f6e2da51cfc9e110bd22a20f3ba10f147e0771b3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
