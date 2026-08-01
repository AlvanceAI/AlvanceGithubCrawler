#!/usr/bin/env bash
set -euo pipefail
base_commit=cde88e9722fe8e2badd5d5eced20f25ac89a9847
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
