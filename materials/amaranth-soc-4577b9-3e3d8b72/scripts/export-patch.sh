#!/usr/bin/env bash
set -euo pipefail
base_commit=3e3d8b7241c1c7e80e0cd12937d288d0ad4a6cba
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
