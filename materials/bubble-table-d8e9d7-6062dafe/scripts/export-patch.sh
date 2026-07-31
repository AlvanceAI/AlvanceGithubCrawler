#!/usr/bin/env bash
set -euo pipefail
base_commit=6062dafe1dd6dcfd8cceb06e54b199b382432605
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
