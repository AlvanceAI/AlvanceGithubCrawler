#!/usr/bin/env bash
set -euo pipefail
cd /app
exec runuser -u user -- env HOME=/home/user PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin sh -c 'python -m pytest -x -q tests/func'
