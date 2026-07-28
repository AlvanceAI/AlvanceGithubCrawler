#!/bin/sh
set -eu
cd /repo
exec env GOCACHE=/root/.cache/go-build GOMODCACHE=/go/pkg/mod GOPATH=/go GOPROXY=https://goproxy.cn,direct GOTOOLCHAIN=go1.26.5+auto HOME=/root PATH=/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin sh -c 'go test ./...'
