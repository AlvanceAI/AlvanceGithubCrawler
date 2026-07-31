#!/usr/bin/env bash
set -euo pipefail
base_commit=f68ef419e622a283e0cf8ddab4498b84f9bd038d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
