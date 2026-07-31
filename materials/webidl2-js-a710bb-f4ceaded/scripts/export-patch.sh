#!/usr/bin/env bash
set -euo pipefail
base_commit=f4ceaded4739406321c219bfe889475071b4e34e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
