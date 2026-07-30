#!/usr/bin/env bash
set -euo pipefail
base_commit=70aa5200fec4731b92709a9541ec9672b7a74335
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
