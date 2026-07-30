#!/usr/bin/env bash
set -euo pipefail
base_commit=ef03827ef6679fb1545e3b93bb758cd9276964d7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
