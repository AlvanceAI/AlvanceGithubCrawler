#!/usr/bin/env bash
set -euo pipefail
base_commit=81f943e15f4f06246dc0870a14aa3915398d0e6d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
