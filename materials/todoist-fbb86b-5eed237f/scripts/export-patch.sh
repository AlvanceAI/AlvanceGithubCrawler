#!/usr/bin/env bash
set -euo pipefail
base_commit=5eed237f383a347c2ed5190f37db73a8b7d7a09e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
