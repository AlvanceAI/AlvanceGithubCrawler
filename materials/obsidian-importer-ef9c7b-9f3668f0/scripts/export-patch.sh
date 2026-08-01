#!/usr/bin/env bash
set -euo pipefail
base_commit=9f3668f0be05ab9bcf73962f767edb39eafa6640
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
