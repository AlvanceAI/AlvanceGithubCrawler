#!/usr/bin/env bash
set -euo pipefail
base_commit=5115ce2bcc8cc3c2f61ae0dbe1d4cbef052bb753
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
