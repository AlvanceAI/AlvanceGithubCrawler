#!/usr/bin/env bash
set -euo pipefail
cd /app
exec env HOME=/root PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin sh -c 'python -m pytest -x -q'
