#!/usr/bin/env bash
set -euo pipefail
base_commit=f898436e37a5c72ed8d2cb7607bd11c42fc57750
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
