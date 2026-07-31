#!/usr/bin/env bash
set -euo pipefail
base_commit=4bd93773f0de54902f88292c3c170eab731589f9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
