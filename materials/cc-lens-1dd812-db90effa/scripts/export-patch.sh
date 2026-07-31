#!/usr/bin/env bash
set -euo pipefail
base_commit=db90effa1b4f3452b6660e7ff6896901b1efdc56
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
