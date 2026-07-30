#!/usr/bin/env bash
set -euo pipefail
base_commit=db4de3f4ede5bbcd0cce4f2b3666027caad3786d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
