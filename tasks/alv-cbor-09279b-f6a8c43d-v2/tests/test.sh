#!/bin/sh
set -u
mkdir -p /logs/verifier
cd /app
if env GOCACHE=/root/.cache/go-build GOMODCACHE=/go/pkg/mod GOPATH=/go GOPROXY=https://goproxy.cn,direct GOTOOLCHAIN=go1.24.0+auto HOME=/root PATH=/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin sh -c 'go test ./...'; then
    echo 1 > /logs/verifier/reward.txt
    exit 0
else
    status=$?
    echo 0 > /logs/verifier/reward.txt
    exit "$status"
fi
