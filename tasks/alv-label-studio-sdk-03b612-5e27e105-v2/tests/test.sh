#!/bin/sh
set -u
mkdir -p /logs/verifier
cd /app
if env HOME=/root PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin sh -c 'python -m pytest -x -q'; then
    echo 1 > /logs/verifier/reward.txt
    exit 0
else
    status=$?
    echo 0 > /logs/verifier/reward.txt
    exit "$status"
fi
