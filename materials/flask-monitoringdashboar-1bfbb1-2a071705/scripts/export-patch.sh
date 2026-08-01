#!/usr/bin/env bash
set -euo pipefail
base_commit=2a07170504d21228e6a42ed42d389bd67634ffeb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
