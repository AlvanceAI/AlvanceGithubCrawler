#!/usr/bin/env bash
set -euo pipefail
base_commit=ee987dd3917fbde8130bd05d6649897dde87523c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
