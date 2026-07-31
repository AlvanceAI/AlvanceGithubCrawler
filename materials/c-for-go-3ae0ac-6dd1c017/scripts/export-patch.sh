#!/usr/bin/env bash
set -euo pipefail
base_commit=6dd1c017f91eea5364499f7926d94583eaddaadb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
