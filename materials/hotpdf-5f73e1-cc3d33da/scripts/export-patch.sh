#!/usr/bin/env bash
set -euo pipefail
base_commit=cc3d33da77639ba56f60423c09c9b46d58d6df39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
