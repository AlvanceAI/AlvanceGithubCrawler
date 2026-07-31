#!/usr/bin/env bash
set -euo pipefail
base_commit=e3dc6026c393d1ef759bc139c0ce95d39c1296a4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
