#!/usr/bin/env bash
set -euo pipefail
base_commit=843c38e886f5749cc03b967f37e6d5fb7a85999a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
