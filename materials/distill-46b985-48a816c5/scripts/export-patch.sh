#!/usr/bin/env bash
set -euo pipefail
base_commit=48a816c5edee15fc6d18edd7872a4d16d6f310cc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
