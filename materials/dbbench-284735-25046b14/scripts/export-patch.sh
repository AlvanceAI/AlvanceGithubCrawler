#!/usr/bin/env bash
set -euo pipefail
base_commit=25046b14084680b51071d8f4f05c1d7e6fff50b9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
