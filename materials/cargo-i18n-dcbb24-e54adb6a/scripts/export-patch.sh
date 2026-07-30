#!/usr/bin/env bash
set -euo pipefail
base_commit=e54adb6a57a91ea4211221bcd54d8dad760b237a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
