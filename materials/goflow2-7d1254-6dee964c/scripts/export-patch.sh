#!/usr/bin/env bash
set -euo pipefail
base_commit=6dee964c38ee5f6b04a38681d069427c28ee5cb3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
