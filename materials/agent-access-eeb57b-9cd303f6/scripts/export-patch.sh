#!/usr/bin/env bash
set -euo pipefail
base_commit=9cd303f65dc501c19d1d513fb4cf88fe5f44936a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
